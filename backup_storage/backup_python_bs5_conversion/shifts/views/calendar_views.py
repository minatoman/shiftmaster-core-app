# shifts/views/calendar_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Shift, ShiftRequest


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


