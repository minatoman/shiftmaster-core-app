# shifts/tests/test_dashboard_chart.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from shifts.models import Employee
import json
from shifts.tests.test_utils import create_test_employee

class DashboardChartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="password123")
        self.client = Client()
        self.client.login(username="admin", password="password123")
        Employee.objects.create(
            name="統計対象者", email="stat@example.com", user=self.user,
            department="外来", position="看護師", employment_type="常勤",
            work_details={"透析": True}
        )

    def test_dashboard_chart_json(self):
        response = self.client.get(reverse('dashboard_chart_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertIn('labels', data)
        self.assertIn('data', data)
