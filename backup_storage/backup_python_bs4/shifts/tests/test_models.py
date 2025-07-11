from django.test import TestCase
from django.contrib.auth.models import User
from shifts.models import Employee, ShiftRequest
from datetime import date
from shifts.tests.test_utils import create_test_employee

class EmployeeModelTestCase(TestCase):
    def setUp(self):
        # テストユーザーを作成
        self.user = User.objects.create_user(username='tanaka', password='testpass')

        # テストデータ（必須フィールドをすべて含む）を準備
        self.employee = Employee.objects.create(
            name="田中",
            email="tanaka@example.com",
            position="看護師",
            department="透析室",
            employment_type="常勤",
            work_details={"main": "透析業務"},  # ★ Null不可フィールド
            user=self.user
        )

    def test_employee_creation(self):
        employee = self.employee
        self.assertEqual(employee.name, "田中")
        self.assertEqual(employee.position, "看護師")
        self.assertTrue(employee.email)


class ShiftRequestModelTestCase(TestCase):
    def setUp(self):
        # テストユーザーとスタッフを準備
        self.user = User.objects.create_user(username='tanaka2', password='testpass2')
        self.employee = Employee.objects.create(
            name="田中",
            email="tanaka@example.com",
            position="看護師",
            department="透析室",
            employment_type="常勤",
            work_details={"main": "透析業務"},
            user=self.user
        )
        self.shift_request = ShiftRequest.objects.create(
            employee=self.employee,
            requested_date=date(2025, 4, 1),
            shift_type="morning",
            priority=1
        )

    def test_shift_request_creation(self):
        shift_request = self.shift_request
        self.assertEqual(shift_request.employee.name, "田中")
        self.assertEqual(shift_request.shift_type, "morning")
        self.assertEqual(shift_request.priority, 1)
