from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date, timedelta, datetime
import json
import calendar

from .models import Employee, Shift, ShiftRequest, ShiftType, Attendance, Notification
from .forms import (
    CustomUserCreationForm, EmployeeForm, ShiftForm, ShiftRequestForm,
    ShiftTypeForm, DateRangeForm, QuickShiftForm, AttendanceForm
)


def home(request):
    """ホーム画面"""
    if request.user.is_authenticated:
        return redirect('shifts:dashboard')
    return render(request, 'shifts/home.html')


def register(request):
    """ユーザー登録"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 従業員レコードを作成
            Employee.objects.create(
                user=user,
                employee_id=f"EMP{user.id:04d}",
                name=f"{user.last_name} {user.first_name}",
                position="未設定",
                email=user.email
            )
            login(request, user)
            messages.success(request, 'アカウントが作成されました。')
            return redirect('shifts:profile_edit')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    """ダッシュボード"""
    employee = request.user.employee
    today = date.today()
    
    # 今日のシフト
    today_shift = Shift.objects.filter(
        employee=employee,
        shift_date=today
    ).first()
    
    # 今週のシフト
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_shifts = Shift.objects.filter(
        employee=employee,
        shift_date__range=[week_start, week_end]
    ).select_related('shift_type').order_by('shift_date')
    
    # 未読通知
    notifications = Notification.objects.filter(
        recipient=employee,
        is_read=False
    ).order_by('-created_at')[:5]
    
    # 申請中のリクエスト
    pending_requests = ShiftRequest.objects.filter(
        requester=employee,
        status='pending'
    ).count()
    
    # 今日の出勤状況
    attendance_today = None
    if today_shift:
        try:
            attendance_today = Attendance.objects.get(shift=today_shift)
        except Attendance.DoesNotExist:
            pass
    
    context = {
        'employee': employee,
        'today_shift': today_shift,
        'week_shifts': week_shifts,
        'notifications': notifications,
        'pending_requests': pending_requests,
        'attendance_today': attendance_today,
        'today': today,
    }
    return render(request, 'shifts/dashboard.html', context)


@login_required
def shift_calendar(request):
    """シフトカレンダー"""
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    
    # カレンダーの日付範囲を計算
    cal = calendar.Calendar(firstweekday=6)  # 日曜日始まり
    month_days = cal.monthdayscalendar(year, month)
    
    # 月のシフトデータを取得
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)
    
    shifts = Shift.objects.filter(
        shift_date__range=[month_start, month_end]
    ).select_related('employee', 'shift_type').order_by('shift_date', 'employee__name')
    
    # 日付別にシフトをグループ化
    shifts_by_date = {}
    for shift in shifts:
        if shift.shift_date not in shifts_by_date:
            shifts_by_date[shift.shift_date] = []
        shifts_by_date[shift.shift_date].append(shift)
    
    # 前月と次月の情報
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_days': month_days,
        'shifts_by_date': shifts_by_date,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    return render(request, 'shifts/calendar.html', context)


@login_required
def shift_list(request):
    """シフト一覧"""
    form = DateRangeForm(request.GET or None)
    shifts = Shift.objects.all().select_related('employee', 'shift_type')
    
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        shifts = shifts.filter(shift_date__range=[start_date, end_date])
    
    shifts = shifts.order_by('-shift_date', 'employee__name')
    
    context = {
        'shifts': shifts,
        'form': form,
    }
    return render(request, 'shifts/shift_list.html', context)


@login_required
def shift_create(request):
    """シフト作成"""
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.requested_by = request.user.employee
            shift.save()
            messages.success(request, 'シフトが作成されました。')
            return redirect('shifts:shift_list')
    else:
        form = ShiftForm()
    
    return render(request, 'shifts/shift_form.html', {'form': form, 'title': 'シフト作成'})


@login_required
def quick_shift_create(request):
    """クイックシフト作成（スマホ対応）"""
    if request.method == 'POST':
        form = QuickShiftForm(request.POST)
        if form.is_valid():
            employees = form.cleaned_data['employees']
            shift_type = form.cleaned_data['shift_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            created_count = 0
            current_date = start_date
            
            while current_date <= end_date:
                for employee in employees:
                    # 既存のシフトがない場合のみ作成
                    if not Shift.objects.filter(employee=employee, shift_date=current_date).exists():
                        Shift.objects.create(
                            employee=employee,
                            shift_date=current_date,
                            shift_type=shift_type,
                            requested_by=request.user.employee,
                            status='approved'
                        )
                        created_count += 1
                current_date += timedelta(days=1)
            
            messages.success(request, f'{created_count}件のシフトが作成されました。')
            return redirect('shifts:calendar')
    else:
        form = QuickShiftForm()
    
    return render(request, 'shifts/quick_shift_form.html', {'form': form})


@login_required
def attendance_punch(request):
    """出勤打刻（スマホ対応）"""
    employee = request.user.employee
    today = date.today()
    
    # 今日のシフトを取得
    today_shift = get_object_or_404(Shift, employee=employee, shift_date=today)
    
    # 出勤記録を取得または作成
    attendance, created = Attendance.objects.get_or_create(shift=today_shift)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            location = form.cleaned_data['location']
            notes = form.cleaned_data['notes']
            now = timezone.now()
            
            if action == 'check_in' and not attendance.check_in_time:
                attendance.check_in_time = now
                messages.success(request, 'チェックインしました。')
            elif action == 'break_start' and not attendance.break_start_time:
                attendance.break_start_time = now
                messages.success(request, '休憩を開始しました。')
            elif action == 'break_end' and attendance.break_start_time and not attendance.break_end_time:
                attendance.break_end_time = now
                messages.success(request, '休憩を終了しました。')
            elif action == 'check_out' and not attendance.check_out_time:
                attendance.check_out_time = now
                messages.success(request, 'チェックアウトしました。')
            else:
                messages.error(request, '無効な操作です。')
                return redirect('shifts:attendance_punch')
            
            if location:
                attendance.location = location
            if notes:
                attendance.notes = notes
            
            attendance.save()
            return redirect('shifts:dashboard')
    else:
        form = AttendanceForm()
    
    context = {
        'form': form,
        'today_shift': today_shift,
        'attendance': attendance,
    }
    return render(request, 'shifts/attendance_punch.html', context)


@login_required
def shift_request_create(request):
    """シフト申請作成"""
    if request.method == 'POST':
        form = ShiftRequestForm(request.POST, user=request.user)
        if form.is_valid():
            shift_request = form.save(commit=False)
            shift_request.requester = request.user.employee
            shift_request.save()
            messages.success(request, 'シフト申請が提出されました。')
            return redirect('shifts:request_list')
    else:
        form = ShiftRequestForm(user=request.user)
    
    return render(request, 'shifts/request_form.html', {'form': form, 'title': 'シフト申請'})


@login_required
def request_list(request):
    """申請一覧"""
    employee = request.user.employee
    requests = ShiftRequest.objects.filter(
        requester=employee
    ).order_by('-created_at')
    
    context = {
        'requests': requests,
    }
    return render(request, 'shifts/request_list.html', context)


@login_required
def profile_edit(request):
    """プロフィール編集"""
    employee = request.user.employee
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールが更新されました。')
            return redirect('shifts:dashboard')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'shifts/profile_edit.html', {'form': form})


@login_required
def notifications(request):
    """通知一覧"""
    employee = request.user.employee
    notifications = Notification.objects.filter(
        recipient=employee
    ).order_by('-created_at')
    
    # 未読通知を既読にする
    Notification.objects.filter(
        recipient=employee,
        is_read=False
    ).update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'shifts/notifications.html', context)


@login_required
def api_shift_data(request):
    """API: シフトデータ（AJAX用）"""
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    if start_date and end_date:
        shifts = Shift.objects.filter(
            shift_date__range=[start_date, end_date]
        ).select_related('employee', 'shift_type')
        
        events = []
        for shift in shifts:
            events.append({
                'id': str(shift.id),
                'title': f"{shift.employee.name} - {shift.shift_type.name}",
                'start': shift.shift_date.isoformat(),
                'backgroundColor': shift.shift_type.color_code,
                'borderColor': shift.shift_type.color_code,
            })
        
        return JsonResponse(events, safe=False)
    
    return JsonResponse([], safe=False)


def mobile_detect(request):
    """モバイルデバイス検出"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'blackberry', 'webos']
    return any(keyword in user_agent for keyword in mobile_keywords)
