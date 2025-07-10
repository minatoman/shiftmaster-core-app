# shifts/tests/test_notify_line.py

from django.test import TestCase
from django.core import mail
from shifts.models import Employee, NotificationLog
from django.contrib.auth.models import User
from django.utils import timezone
from shifts.tests.test_utils import create_test_employee

class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com')
        self.employee = Employee.objects.create(
            name="通知テスト", email="notify@example.com", user=self.user,
            department="透析室", position="看護師", employment_type="常勤",
            work_details={"業務A": True}
        )

    def test_line_notification_log(self):
        # 通知ログの作成シミュレーション
        NotificationLog.objects.create(
            recipient=self.employee.email,
            message="LINE通知テスト",
            method="line"
        )
        logs = NotificationLog.objects.filter(recipient="notify@example.com")
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].message, "LINE通知テスト")
        self.assertEqual(logs[0].method, "line")

