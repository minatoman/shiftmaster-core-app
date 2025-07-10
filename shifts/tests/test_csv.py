import io
import pandas as pd
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shifts.models import DialysisPatient
from shifts.tests.test_utils import create_test_employee

class CSVImportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.client.login(username='admin', password='adminpass')

    def test_import_dialysis_csv(self):
        df = pd.DataFrame([{
            '名前': '患者A',
            '透析時間': 'AM',
            '性別': '男',
            '地域': 'Aエリア',
            '日付': '2025-04-01'
        }])
        file = io.BytesIO()
        with pd.ExcelWriter(file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        file.seek(0)
        response = self.client.post(reverse('import_dialysis_csv'), {'file': file}, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DialysisPatient.objects.count(), 1)

