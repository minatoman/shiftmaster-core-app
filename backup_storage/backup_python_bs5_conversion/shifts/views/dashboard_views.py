# shifts/views/dashboard_views.py

import json
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.urls import reverse

from shifts.models import Shift, Employee, ShiftRequest, HolidayRequest


# 🔐 管理者アクセス専用のデコレータ
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


# 👥 通常ユーザー用：ダッシュボード（リンク一覧）
@login_required
def dashboard_view(request):
    links = [
        {"title": "📋 シフト一覧", "url": reverse("shifts:shift_list"), "label": "シフト管理"},
        {"title": "📆 勤務希望一覧", "url": reverse("shifts:shift_request_list"), "label": "希望一覧"},
        {"title": "🛌 休暇申請", "url": reverse("shifts:add_holiday_request"), "label": "休暇申請"},
        {"title": "📊 月次統計", "url": reverse("shifts:monthly_shift_summary"), "label": "統計表示"},
        {"title": "🖨️ PDF出力", "url": reverse("shifts:export_shift_pdf"), "label": "PDF出力"},
        {"title": "📅 カレンダー", "url": reverse("shifts:calendar_view"), "label": "カレンダー"},
        {"title": "💉 透析登録", "url": reverse("shifts:dialysis_register"), "label": "透析登録"},
        {"title": "📘 透析日誌", "url": reverse("shifts:dialysis_daily"), "label": "透析日誌"},
        {"title": "🧩 テンプレート", "url": reverse("shifts:shift_template_3block"), "label": "テンプレート表示"},
        {"title": "⚙️ 管理画面", "url": reverse("admin:index"), "label": "Django Admin"},
        {"title": "📂 CSVアップ", "url": reverse("shifts:upload_shifts_csv"), "label": "CSV取込"},
    ]
    return render(request, 'shifts/dashboard.html', {'links': links})


# 📊 管理者用：グラフ付きダッシュボード（統計 + 状況表示）
@staff_required
def admin_dashboard(request):
    today = date.today()
    year, month = today.year, today.month

    # データ取得
    shifts = Shift.objects.all().order_by('-shift_date')
    unapproved = ShiftRequest.objects.filter(
        approved=False,
        requested_date__lte=today,
        employee__isnull=False,
        shift_type__isnull=False
    )
    employees = Employee.objects.all()

    # 提出済み勤務希望数（当月）
    submitted_ids = ShiftRequest.objects.filter(
        requested_date__year=year,
        requested_date__month=month
    ).values_list('employee_id', flat=True).distinct()

    # 休暇申請数（当月）
    holiday_requests_count = HolidayRequest.objects.filter(
        holiday_date__year=year,
        holiday_date__month=month
    ).count()

    # 📊 月別 × 職種別 件数（Chart.js用）
    monthly_summary = Shift.objects.values('employee__position', month=TruncMonth('shift_date')) \
        .annotate(count=Count('id')).order_by('month', 'employee__position')

    chart_data = {}
    for entry in monthly_summary:
        month_key = entry['month'].strftime('%Y-%m')
        role = entry['employee__position']
        chart_data.setdefault(month_key, {})[role] = entry['count']

    context = {
        "today": today,
        "shifts": shifts,
        "unapproved": unapproved,
        "employees": employees,
        "total_requests": ShiftRequest.objects.count(),
        "total_shifts": shifts.count(),
        "pending_shifts_count": unapproved.count(),
        "shift_request_submitted": len(submitted_ids),
        "total_employees": employees.count(),
        "holiday_requests_count": holiday_requests_count,
        "chart_data": json.dumps(chart_data),
    }

    return render(request, "shifts/admin_dashboard.html", context)


# 📈 Chart.js用データAPI（月×職種 件数集計）
@staff_required
def dashboard_chart_json(request):
    monthly_summary = Shift.objects.values('employee__position', month=TruncMonth('shift_date')) \
        .annotate(count=Count('id')).order_by('month', 'employee__position')

    chart_data = {}
    for entry in monthly_summary:
        month_key = entry['month'].strftime('%Y-%m')
        role = entry['employee__position']
        chart_data.setdefault(month_key, {})[role] = entry['count']

    return JsonResponse(chart_data)

