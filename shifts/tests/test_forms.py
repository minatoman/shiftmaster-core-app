from django.test import TestCase
from shifts.forms import ShiftRequestForm
from shifts.models import Employee
from django.contrib.auth.models import User
from shifts.tests.test_utils import create_test_employee

class ShiftRequestFormTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        self.employee = Employee.objects.create(
            name='田中',
            email='t@example.com',
            user=user,
            position='看護師',
            department='透析室',
            work_details={"業務": "透析"}
        )

    def test_valid_shift_request_form(self):
        form_data = {
            'employee': self.employee.id,
            'requested_date': '2025-04-15',
            'shift_type': 'morning',
            'priority': 1,
        }
        form = ShiftRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

