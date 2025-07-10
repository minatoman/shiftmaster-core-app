from shifts.models import ShiftRequest, Shift, ShiftRequirement
from django.db.models import Count

assigned_count = 0

for req in ShiftRequest.objects.all():
    # その日、その職種ですでに割り当てられている数を取得
    shift_date = req.requested_date
    job = req.employee.position
    day_of_week = shift_date.strftime('%A')  # 例：'Monday'

    try:
        requirement = ShiftRequirement.objects.get(day_of_week=day_of_week)
        existing_count = Shift.objects.filter(shift_date=shift_date, employee__position=job).count()

        # 上限確認
        limit = getattr(requirement, f"{'nurse' if job == '看護師' else 'engineer' if job == '臨床工学技士' else 'assistant'}_required")

        if existing_count < limit:
            if not Shift.objects.filter(employee=req.employee, shift_date=shift_date).exists():
                Shift.objects.create(
                    employee=req.employee,
                    shift_date=shift_date,
                    shift_type=req.shift_type,
                    is_approved=True
                )
                assigned_count += 1

    except ShiftRequirement.DoesNotExist:
        print(f"⚠ 要件未定義：{day_of_week}")

print(f"✅ 自動割当完了：{assigned_count} 件のシフトを登録しました。")
