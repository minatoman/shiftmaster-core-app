from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shifts.models import DialysisPatient
from shifts.tests.test_utils import create_test_employee

class PDFExportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass', is_staff=True)
        self.client.login(username='testuser', password='testpass')
        DialysisPatient.objects.create(
            name="患者X",
            dialysis_time="PM",
            gender="女",
            area="地域A",
            date="2025-04-15"
        )

    def test_pdf_export(self):
        response = self.client.get(reverse('dialysis_pdf_export', args=['2025-04-15']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
