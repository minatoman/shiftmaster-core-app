
import csv, io, json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ShiftRequest, HolidayRequest, Employee

@login_required
def upload_shift_requests_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        decoded = file.read().decode("utf-8-sig")
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)
        for row in reader:
            employee = Employee.objects.get(name=row['employee'])
            ShiftRequest.objects.create(
                employee=employee,
                requested_date=row['requested_date'],
                shift_type=row['shift_type'],
                priority=int(row['priority']),
                approved=row['approved'].lower() in ['true', '1']
            )
        messages.success(request, "勤務希望CSVを登録しました。")
        return redirect("shift_list")
    return render(request, "shifts/upload_shift_requests.html")

@login_required
def upload_holiday_requests_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        decoded = file.read().decode("utf-8-sig")
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)
        for row in reader:
            employee = Employee.objects.get(name=row['employee'])
            HolidayRequest.objects.create(
                employee=employee,
                holiday_date=row['holiday_date'],
                holiday_type=row['holiday_type']
            )
        messages.success(request, "休暇希望CSVを登録しました。")
        return redirect("shift_list")
    return render(request, "shifts/upload_holiday_requests.html")
