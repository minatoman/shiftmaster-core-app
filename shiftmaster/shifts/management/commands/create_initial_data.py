from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shifts.models import Employee, ShiftType
from datetime import time, timedelta


class Command(BaseCommand):
    help = 'Create initial data for ShiftMaster'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data...')
        
        # Create shift types
        shift_types = [
            {
                'name': '日勤',
                'start_time': time(9, 0),
                'end_time': time(17, 0),
                'break_time': timedelta(hours=1),
                'color_code': '#007bff'
            },
            {
                'name': '夜勤',
                'start_time': time(21, 0),
                'end_time': time(6, 0),
                'break_time': timedelta(hours=2),
                'color_code': '#6f42c1'
            },
            {
                'name': '準夜勤',
                'start_time': time(16, 0),
                'end_time': time(1, 0),
                'break_time': timedelta(hours=1),
                'color_code': '#fd7e14'
            },
            {
                'name': '早番',
                'start_time': time(7, 0),
                'end_time': time(15, 0),
                'break_time': timedelta(hours=1),
                'color_code': '#28a745'
            },
            {
                'name': '遅番',
                'start_time': time(11, 0),
                'end_time': time(19, 0),
                'break_time': timedelta(hours=1),
                'color_code': '#17a2b8'
            },
            {
                'name': '有休',
                'start_time': time(0, 0),
                'end_time': time(0, 0),
                'break_time': timedelta(0),
                'color_code': '#6c757d'
            },
            {
                'name': '研修',
                'start_time': time(9, 0),
                'end_time': time(17, 0),
                'break_time': timedelta(hours=1),
                'color_code': '#e83e8c'
            }
        ]
        
        for shift_data in shift_types:
            shift_type, created = ShiftType.objects.get_or_create(
                name=shift_data['name'],
                defaults=shift_data
            )
            if created:
                self.stdout.write(f'Created shift type: {shift_type.name}')
            else:
                self.stdout.write(f'Shift type already exists: {shift_type.name}')
        
        # Create demo employees if none exist
        if not Employee.objects.exists():
            demo_employees = [
                {
                    'username': 'nurse001',
                    'first_name': '花子',
                    'last_name': '田中',
                    'email': 'nurse001@example.com',
                    'position': '看護師',
                    'department': '内科'
                },
                {
                    'username': 'nurse002',
                    'first_name': '太郎',
                    'last_name': '佐藤',
                    'email': 'nurse002@example.com',
                    'position': '看護師',
                    'department': '外科'
                },
                {
                    'username': 'assist001',
                    'first_name': '美咲',
                    'last_name': '鈴木',
                    'email': 'assist001@example.com',
                    'position': '看護補助',
                    'department': '内科'
                }
            ]
            
            for emp_data in demo_employees:
                user = User.objects.create_user(
                    username=emp_data['username'],
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    email=emp_data['email'],
                    password='demo2025'
                )
                
                employee = Employee.objects.create(
                    user=user,
                    employee_id=f"EMP{user.id:04d}",
                    name=f"{emp_data['last_name']} {emp_data['first_name']}",
                    position=emp_data['position'],
                    department=emp_data['department'],
                    email=emp_data['email']
                )
                
                self.stdout.write(f'Created demo employee: {employee.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created initial data!')
        )
