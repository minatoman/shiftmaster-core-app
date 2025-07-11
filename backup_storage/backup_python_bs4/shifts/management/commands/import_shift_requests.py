
import pandas as pd
import json
from django.core.management.base import BaseCommand
from shifts.models import ShiftRequest, Employee

class Command(BaseCommand):
    help = 'CSVからShiftRequest（勤務希望）データを読み込んで登録する'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('shifts/shift_requests_template.csv')

        for _, row in df.iterrows():
            try:
                employee = Employee.objects.get(email=row['employee_email'])
                ShiftRequest.objects.update_or_create(
                    employee=employee,
                    requested_date=row['requested_date'],
                    shift_type=row['shift_type'],
                    defaults={
                        'priority': int(row.get('priority', 1)),
                        'approved': str(row.get('approved', False)).lower() in ['true', '1']
                    }
                )
                self.stdout.write(f"✔ 登録完了: {employee.name} - {row['requested_date']}")
            except Employee.DoesNotExist:
                self.stdout.write(f"⚠ スキップ: 該当する社員が見つかりません - {row['employee_email']}")
