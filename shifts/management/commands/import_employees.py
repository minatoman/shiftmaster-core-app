# shifts/management/commands/import_employees.py
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from shifts.models import Employee

class Command(BaseCommand):
    help = 'CSVファイルから従業員データをインポート'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'shifts', 'csv', 'employees.csv')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSVファイルが見つかりません: {csv_path}"))
            return

        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            created_count = 0

            for row in reader:
                if Employee.objects.filter(email=row['email']).exists():
                    self.stdout.write(f"スキップ（既に存在）: {row['email']}")
                    continue

                user = User.objects.create_user(
                    username=row['email'],
                    email=row['email'],
                    password=row.get('password', 'shiftpass123')  # 仮パスワード
                )

                emp = Employee.objects.create(
                    user=user,
                    name=row['name'],
                    name_kana=row.get('name_kana'),
                    gender=row.get('gender'),
                    birth_date=row.get('birth_date') or None,
                    email=row['email'],
                    phone=row.get('phone'),
                    department=row.get('department'),
                    assigned_locations=row.get('assigned_locations', '{}'),
                    position=row['position'],
                    employment_type=row.get('employment_type'),
                    hire_date=row.get('hire_date') or None,
                    work_details=row.get('work_details', '{}'),
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'{created_count} 件の従業員をインポートしました。'))
