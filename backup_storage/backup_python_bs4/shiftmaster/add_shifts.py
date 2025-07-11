import os
import django
from datetime import datetime

# Djangoの設定をロード
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiftmaster.settings')
django.setup()

from shifts.models import Shift, Employee

# シフトデータ
shifts = [
    {'name': '神 道人', 'shift_dates': '2025-04-01,2025-04-02,2025-04-03', 'shift_types': '勤務,勤務,勤務', 'position': '看護師'},
    {'name': '大谷 興', 'shift_dates': '2025-04-04,2025-04-05', 'shift_types': '整形,ＮＳ勤務', 'position': '看護師'}, 
    {'name': '木村 陽子', 'shift_dates': '2025-04-06,2025-04-07', 'shift_types': '有休,ＮＳ勤務', 'position': '看護補助'},
    {'name': '渥美 大五', 'shift_dates': '2025-04-08,2025-04-09', 'shift_types': 'ＮＳ勤務,ＮＳ勤務残', 'position': '臨床工学技士'},
    {'name': '寺島 靖人', 'shift_dates': '2025-04-10,2025-04-11', 'shift_types': 'ＮＳ勤務,代休', 'position': '看護師'}
]

# データ追加処理
for shift in shifts:
    # 従業員が存在しない場合は作成
    employee, created = Employee.objects.get_or_create(
        name=shift['name'],
        defaults={'position': shift['position']}
    )
    
    for date_str, shift_type in zip(shift['shift_dates'].split(','), shift['shift_types'].split(','):
        shift_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        Shift.objects.create(
            employee=employee, 
            shift_date=shift_date, 
            shift_type=shift_type.strip(), 
            is_approved=True
        )
        print(f"Added shift for {employee.name} on {shift_date}: {shift_type}")