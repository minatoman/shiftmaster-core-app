
import pandas as pd
from django.core.management.base import BaseCommand
from shifts.models import HolidayRequest, Employee

class Command(BaseCommand):
    help = 'CSVからHolidayRequest（休暇希望）データを読み込んで登録する'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('shifts/holiday_requests_template.csv')

        for _, row in df.iterrows():
            try:
                employee = Employee.objects.get(email=row['employee_email'])
                HolidayRequest.objects.update_or_create(
                    employee=employee,
                    holiday_date=row['holiday_date'],
                    defaults={
                        'holiday_type': row['holiday_type']
                    }
                )
                self.stdout.write(f"✔ 登録完了: {employee.name} - {row['holiday_date']}")
            except Employee.DoesNotExist:
                self.stdout.write(f"⚠ スキップ: 該当する社員が見つかりません - {row['employee_email']}")
