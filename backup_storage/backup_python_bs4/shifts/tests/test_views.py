from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shifts.models import Employee, Shift
from shifts.tests.test_utils import create_test_employee

class ShiftViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.employee = Employee.objects.create(
            name="田中",
            email="tanaka@example.com",
            user=self.user,
            position="看護師",
            department="透析室",
            work_details={"業務": "透析看護"}
        )

    def test_shift_register_view_requires_login(self):
        response = self.client.get(reverse('shift_register'))
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('shift_register'))

    def test_shift_register_post(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'form-0-employee': self.employee.id,
            'form-0-shift_date': '2025-04-20',
            'form-0-shift_type': 'morning',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
        }
        response = self.client.post(reverse('shift_register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Shift.objects.count(), 1)
