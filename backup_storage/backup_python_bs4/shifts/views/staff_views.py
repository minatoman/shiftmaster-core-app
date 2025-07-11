# shifts/views/staff_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.template.loader import get_template
import os
import io
import csv
import json
import calendar
from datetime import datetime
from collections import defaultdict

from ..models import Shift, ShiftRequest, Employee, ShiftRequirement
from ..forms import ShiftForm, EmployeeForm
from ..utils import normalize_name

# --- 権限チェック ---
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

# --- シフト管理ビュー ---
@login_required
def shift_list(request):
    shifts = Shift.objects.all()
    employee_name = request.GET.get("employee")
    date = request.GET.get("date")
    shift_type = request.GET.get("shift_type")

    if employee_name:
        shifts = shifts.filter(employee__name__icontains=employee_name)
    if date:
        shifts = shifts.filter(shift_date=date)
    if shift_type:
        shifts = shifts.filter(shift_type__icontains=shift_type)

    return render(request, 'shifts/shift_list.html', {'shifts': shifts})

@login_required
def add_shift(request):
    form = ShiftForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '新しいシフトが追加されました！')
        return redirect('shifts:shift_list')
    return render(request, 'shifts/add_shift.html', {'form': form})

@login_required
def edit_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            messages.success(request, 'シフトが更新されました。')
            return redirect('shifts:shift_list')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'shifts/edit_shift.html', {'form': form, 'shift': shift})

@login_required
def delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        shift.delete()
        messages.success(request, f"シフト {shift.employee.name} - {shift.shift_date} が削除されました。")
        return redirect('shifts:shift_list')
    return render(request, 'shifts/confirm_delete_shift.html', {'shift': shift})

@login_required
def confirm_delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    return render(request, 'shifts/confirm_delete_shift.html', {'shift': shift})

@login_required
def approve_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        shift.is_approved = True
        shift.save()
        messages.success(request, f"シフト {shift.employee.name} - {shift.shift_date} が承認されました。")
        return redirect('shifts:shift_list')
    return render(request, 'shifts/approve_shift.html', {'shift': shift})

@staff_required
def auto_assign(request):
    assigned = set()
    assigned_counts = defaultdict(lambda: defaultdict(int))
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
        week_day_index = list(calendar.day_name).index(day) + 2
        requests = ShiftRequest.objects.filter(requested_date__week_day=week_day_index).order_by('priority')
        requirements = ShiftRequirement.objects.filter(day_of_week=day).first()
        if not requirements:
            continue
        counts = {
            '看護師': requirements.nurse_required,
            '臨床工学技士': requirements.engineer_required,
            '介護福祉士': requirements.assistant_required
        }
        for req in requests:
            emp_id = req.employee.id
            date_key = (emp_id, req.requested_date)
            position = req.employee.position
            if counts.get(position, 0) > 0 and date_key not in assigned:
                Shift.objects.create(
                    employee=req.employee,
                    shift_date=req.requested_date,
                    shift_type=req.shift_type,
                    is_approved=True
                )
                assigned.add(date_key)
                assigned_counts[emp_id][day] += 1
                counts[position] -= 1
    messages.success(request, '最適化された勤務割当が完了しました。')
    return redirect('shifts:shift_list')


# --- スタッフ管理ビュー ---
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'staff/employee_list.html', {'employees': employees})

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'スタッフを登録しました。')
            return redirect('staff:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'staff/employee_form.html', {'form': form})

@login_required
def upload_employee_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            try:
                user, _ = User.objects.get_or_create(username=row['user'], defaults={'email': row['email']})
                Employee.objects.create(
                    name=row['name'],
                    name_kana=row.get('name_kana') or '',
                    gender=row.get('gender') or '',
                    birth_date=parse_date(row.get('birth_date')),
                    email=row['email'],
                    phone=row.get('phone') or '',
                    user=user,
                    department=row['department'],
                    assigned_locations=json.loads(row['assigned_locations'] or '{}'),
                    position=row['position'],
                    employment_type=row['employment_type'],
                    hire_date=parse_date(row['hire_date']),
                    work_constraints=json.loads(row.get('work_constraints') or '{}'),
                    qualifications=json.loads(row.get('qualifications') or '[]'),
                    work_details=json.loads(row['work_details']),
                    committees=json.loads(row.get('committees') or '[]'),
                    teams=json.loads(row.get('teams') or '[]'),
                    clinical_ladder=row.get('clinical_ladder') or '',
                    yearly_goals=row.get('yearly_goals') or '',
                    career_history=row.get('career_history') or '',
                    ability_rating=json.loads(row.get('ability_rating') or '{}'),
                    performance_evaluation=json.loads(row.get('performance_evaluation') or '{}'),
                    admin_notes=row.get('admin_notes') or '',
                    interview_history=json.loads(row.get('interview_history') or '[]'),
                    notes=row.get('notes') or '',
                    is_active=row.get('is_active', 'TRUE').upper() == 'TRUE'
                )
            except Exception as e:
                messages.error(request, f"エラー: {e}")
                continue

        messages.success(request, 'CSVからスタッフ情報をインポートしました。')
        return redirect('staff:employee_list')

    return render(request, 'staff/upload_employee_csv.html')


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'スタッフ情報を更新しました。')
            return redirect('staff:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'staff/employee_edit.html', {'form': form, 'employee': employee})

@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'staff/employee_detail.html', {'employee': employee})

@login_required
def delete_duplicates(request):
    seen = set()
    duplicates = []
    for emp in Employee.objects.all():
        if emp.name in seen:
            duplicates.append(emp)
        else:
            seen.add(emp.name)
    for dup in duplicates:
        dup.delete()
    messages.success(request, f"{len(duplicates)} 件の重複従業員を削除しました。")
    return redirect('staff:employee_list')

@staff_required
def upload_fixture(request):
    if request.method == 'POST' and request.FILES.get('data_file'):
        data_file = request.FILES['data_file']
        ext = data_file.name.split('.')[-1].lower()

        try:
            if ext == 'json':
                data = json.load(data_file)
                created_count = 0
                for entry in data:
                    fields = entry.get("fields", entry)
                    obj, created = Employee.objects.update_or_create(
                        name=fields.get("name"),
                        defaults=fields
                    )
                    if created:
                        created_count += 1
                messages.success(request, f"✅ JSONから {created_count} 件登録しました。")
            elif ext == 'csv':
                decoded_file = data_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                created_count = 0
                for row in reader:
                    for k in ['assigned_locations', 'work_constraints', 'qualifications',
                              'work_details', 'committees', 'teams', 'ability_rating',
                              'performance_evaluation', 'interview_history']:
                        if row.get(k):
                            try:
                                row[k] = json.loads(row[k])
                            except Exception:
                                row[k] = {}

                    row['hire_date'] = parse_date(row.get('hire_date')) if row.get('hire_date') else None
                    row['birth_date'] = parse_date(row.get('birth_date')) if row.get('birth_date') else None
                    row['is_active'] = row.get('is_active', 'TRUE').upper() == 'TRUE'

                    obj, created = Employee.objects.update_or_create(
                        name=row.get("name"),
                        defaults=row
                    )
                    if created:
                        created_count += 1

                messages.success(request, f"✅ CSVから {created_count} 件登録しました。")
            else:
                messages.error(request, "対応していないファイル形式です（.json または .csv のみ）")
        except Exception as e:
            messages.error(request, f"エラーが発生しました: {str(e)}")

        return redirect('staff:employee_list')

    return render(request, 'staff/upload_fixture.html')
