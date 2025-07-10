# shifts/views/calendar_views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Shift, ShiftRequest, Employee


@login_required
def calendar_view(request):
    return render(request, 'shifts/calendar_full.html')


@login_required
def calendar_event_api(request):
    events = []
    for shift in Shift.objects.all():
        events.append({
            "title": f"[確定] {shift.employee.name}（{shift.shift_type}）",
            "start": str(shift.shift_date),
            "color": "#007bff"
        })
    for req in ShiftRequest.objects.all():
        events.append({
            "title": f"[希望] {req.employee.name}（{req.shift_type}）",
            "start": str(req.requested_date),
            "color": "#28a745"
        })
    return JsonResponse(events, safe=False)


# ✅ 従業員の勤務スケジュールを表示するビュー
@login_required
def my_schedule(request, employee_id):
    """
    従業員の勤務スケジュールを表示するビュー
    """
    # 従業員情報を取得
    employee = get_object_or_404(Employee, id=employee_id)
    
    # 従業員の勤務スケジュールを取得
    shifts = Shift.objects.filter(employee=employee).order_by('shift_date')
    
    return render(request, 'shifts/my_schedule.html', {
        'employee': employee,
        'shifts': shifts
    })
