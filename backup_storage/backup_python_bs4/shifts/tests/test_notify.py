from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from shifts.utils import send_line_notification
from shifts.models import Employee
from shifts.tests.test_utils import create_test_employee


class LineNotificationTestCase(TestCase):
    def setUp(self):
        # テスト用のEmployeeインスタンスを作成
        self.employee = create_test_employee()
        self.employee.line_notify_token = "dummy_token"
        self.employee.save()

    @patch('shifts.utils.requests.post')
    def test_send_line_notification_success(self, mock_post):
        """
        通知成功時の動作検証（status_code = 200）
        """
        mock_post.return_value.status_code = 200
        result = send_line_notification("テスト通知です。", self.employee.line_notify_token)
        self.assertTrue(result)

    @patch('shifts.utils.requests.post')
    def test_send_line_notification_failure(self, mock_post):
        """
        通知失敗時の動作検証（status_code ≠ 200）
        """
        mock_post.return_value.status_code = 400
        result = send_line_notification("失敗通知テスト", self.employee.line_notify_token)
        self.assertFalse(result)

    def test_send_line_notification_without_token(self):
        """
        トークン未設定時のエラー処理検証
        """
        result = send_line_notification("トークンなし通知", None)
        self.assertFalse(result)
