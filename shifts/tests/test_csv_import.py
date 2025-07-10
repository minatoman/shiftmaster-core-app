# shifts/tests/test_csv_import.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from io import BytesIO
import pandas as pd
from shifts.tests.test_utils import create_test_employee

class CSVImportTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.client = Client()
        self.client.login(username="admin", password="adminpass")

    def test_csv_upload(self):
        df = pd.DataFrame([{
            "名前": "田中 太郎",
            "透析時間": "4時間",
            "性別": "男",
            "地域": "A区",
            "日付": "2025-04-18"
        }])
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)

        response = self.client.post(reverse('import_dialysis_csv'), {
            'file': excel_file
        }, format='multipart')

        self.assertEqual(response.status_code, 302)  # リダイレクト確認

