"""
Integration Tests for ShiftMaster
統合テスト - 実際のワークフローをテスト
"""

import pytest
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
import json

from shifts.models import Employee, Shift, ShiftAssignment, Attendance
from shifts.models.master_data import Department, Position, ShiftType


class ShiftManagementIntegrationTest(TransactionTestCase):
    """シフト管理統合テスト"""

    def setUp(self):
        """テストデータ準備"""
        # 部署・役職・シフト種別作成
        self.department = Department.objects.create(
            name="内科", code="INT", description="内科部門"
        )

        self.position = Position.objects.create(
            name="看護師",
            code="NURSE",
            description="看護師職",
            department=self.department,
        )

        self.shift_type = ShiftType.objects.create(
            name="日勤",
            code="DAY",
            start_time="09:00",
            end_time="17:00",
            required_staff=3,
        )

        # ユーザー・従業員作成
        self.manager_user = User.objects.create_user(
            username="manager", email="manager@hospital.com", password="testpass123"
        )

        self.nurse_user = User.objects.create_user(
            username="nurse1", email="nurse1@hospital.com", password="testpass123"
        )

        self.manager = Employee.objects.create(
            user=self.manager_user,
            employee_id="MGR001",
            first_name="管理",
            last_name="太郎",
            email="manager@hospital.com",
            department=self.department,
            position=self.position,
            is_manager=True,
        )

        self.nurse = Employee.objects.create(
            user=self.nurse_user,
            employee_id="NUR001",
            first_name="看護",
            last_name="花子",
            email="nurse1@hospital.com",
            department=self.department,
            position=self.position,
        )

    def test_complete_shift_workflow(self):
        """完全なシフトワークフローテスト"""

        # 1. シフト作成
        shift_date = timezone.now().date() + timedelta(days=7)
        shift = Shift.objects.create(
            date=shift_date,
            shift_type=self.shift_type,
            department=self.department,
            required_staff=2,
            created_by=self.manager,
        )

        # 2. シフト割り当て
        assignment = ShiftAssignment.objects.create(
            shift=shift,
            employee=self.nurse,
            assigned_by=self.manager,
            status="confirmed",
        )

        # 3. 出勤記録
        start_datetime = timezone.make_aware(
            datetime.combine(shift_date, datetime.strptime("09:00", "%H:%M").time())
        )
        end_datetime = timezone.make_aware(
            datetime.combine(shift_date, datetime.strptime("17:00", "%H:%M").time())
        )

        attendance = Attendance.objects.create(
            employee=self.nurse,
            shift=shift,
            clock_in_time=start_datetime,
            clock_out_time=end_datetime,
            status="completed",
        )

        # 4. 検証
        self.assertEqual(shift.assignments.count(), 1)
        self.assertEqual(assignment.employee, self.nurse)
        self.assertEqual(attendance.work_hours, 8.0)
        self.assertEqual(attendance.status, "completed")

    def test_api_workflow(self):
        """API統合テスト"""

        # 認証
        self.client.login(username="manager", password="testpass123")

        # 1. シフト一覧取得
        response = self.client.get(reverse("shifts:shift-list"))
        self.assertEqual(response.status_code, 200)

        # 2. シフト作成API
        shift_data = {
            "date": (timezone.now().date() + timedelta(days=7)).isoformat(),
            "shift_type": self.shift_type.id,
            "department": self.department.id,
            "required_staff": 2,
        }

        response = self.client.post(
            reverse("shifts:shift-create"),
            data=json.dumps(shift_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        # 3. 作成されたシフトID取得
        shift_id = response.json()["id"]

        # 4. シフト割り当てAPI
        assignment_data = {"shift": shift_id, "employee": self.nurse.id}

        response = self.client.post(
            reverse("shifts:assignment-create"),
            data=json.dumps(assignment_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_notification_workflow(self):
        """通知システム統合テスト"""
        from shifts.models.notifications import Notification, NotificationTemplate

        # 通知テンプレート作成
        template = NotificationTemplate.objects.create(
            name="shift_assignment",
            title="シフト割り当て通知",
            content="{{employee_name}}さん、{{shift_date}}の{{shift_type}}シフトに割り当てられました。",
            notification_type="shift_assignment",
        )

        # シフト作成
        shift_date = timezone.now().date() + timedelta(days=7)
        shift = Shift.objects.create(
            date=shift_date,
            shift_type=self.shift_type,
            department=self.department,
            required_staff=2,
            created_by=self.manager,
        )

        # シフト割り当て（通知トリガー）
        assignment = ShiftAssignment.objects.create(
            shift=shift,
            employee=self.nurse,
            assigned_by=self.manager,
            status="confirmed",
        )

        # 通知作成
        notification = Notification.objects.create(
            template=template,
            recipient=self.nurse.user,
            title=f"シフト割り当て通知",
            content=f"{self.nurse.first_name}さん、{shift_date}の{self.shift_type.name}シフトに割り当てられました。",
            notification_type="shift_assignment",
            related_object_id=assignment.id,
        )

        # 検証
        self.assertEqual(
            Notification.objects.filter(recipient=self.nurse.user).count(), 1
        )
        self.assertIn(self.nurse.first_name, notification.content)


class AttendanceWorkflowTest(TransactionTestCase):
    """勤怠管理ワークフローテスト"""

    def setUp(self):
        """テストデータ準備"""
        self.department = Department.objects.create(name="外科", code="SUR")
        self.position = Position.objects.create(
            name="医師", code="DOC", department=self.department
        )
        self.shift_type = ShiftType.objects.create(
            name="夜勤",
            code="NIGHT",
            start_time="21:00",
            end_time="06:00",
            required_staff=2,
        )

        self.user = User.objects.create_user("doctor1", "doc@hospital.com", "pass123")
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id="DOC001",
            first_name="医師",
            last_name="一郎",
            email="doc@hospital.com",
            department=self.department,
            position=self.position,
        )

    def test_overtime_calculation(self):
        """残業時間計算テスト"""
        from shifts.models.attendance import AttendanceRule

        # 勤怠ルール作成
        rule = AttendanceRule.objects.create(
            name="標準勤務ルール",
            normal_work_hours=8.0,
            overtime_threshold=8.0,
            night_shift_allowance=1000,
            is_active=True,
        )

        # シフト作成
        shift_date = timezone.now().date()
        shift = Shift.objects.create(
            date=shift_date,
            shift_type=self.shift_type,
            department=self.department,
            required_staff=1,
        )

        # 長時間勤務の出勤記録
        start_time = timezone.make_aware(
            datetime.combine(shift_date, datetime.strptime("21:00", "%H:%M").time())
        )
        # 2時間残業
        end_time = timezone.make_aware(
            datetime.combine(
                shift_date + timedelta(days=1),
                datetime.strptime("08:00", "%H:%M").time(),
            )
        )

        attendance = Attendance.objects.create(
            employee=self.employee,
            shift=shift,
            clock_in_time=start_time,
            clock_out_time=end_time,
            attendance_rule=rule,
        )

        # 残業時間検証
        self.assertEqual(attendance.work_hours, 11.0)  # 21:00-08:00 = 11時間
        self.assertEqual(attendance.overtime_hours, 3.0)  # 8時間超過分
        self.assertTrue(attendance.is_overtime)

    def test_attendance_correction_workflow(self):
        """勤怠修正ワークフローテスト"""
        from shifts.models.attendance import AttendanceCorrection

        # 初期出勤記録
        shift_date = timezone.now().date()
        shift = Shift.objects.create(
            date=shift_date,
            shift_type=self.shift_type,
            department=self.department,
            required_staff=1,
        )

        attendance = Attendance.objects.create(
            employee=self.employee,
            shift=shift,
            clock_in_time=timezone.now(),
            clock_out_time=timezone.now() + timedelta(hours=8),
            status="completed",
        )

        # 修正申請
        correction = AttendanceCorrection.objects.create(
            attendance=attendance,
            requested_by=self.employee,
            field_name="clock_out_time",
            original_value=attendance.clock_out_time.isoformat(),
            corrected_value=(
                attendance.clock_out_time + timedelta(hours=1)
            ).isoformat(),
            reason="打刻忘れのため1時間遅れで記録",
            status="pending",
        )

        # 承認者による承認
        manager_user = User.objects.create_user("manager", "mgr@hospital.com", "pass")
        manager = Employee.objects.create(
            user=manager_user,
            employee_id="MGR001",
            first_name="管理者",
            last_name="太郎",
            department=self.department,
            position=self.position,
            is_manager=True,
        )

        correction.approve(manager, "システム障害による修正を承認")

        # 検証
        self.assertEqual(correction.status, "approved")
        self.assertEqual(correction.approved_by, manager)
        self.assertIsNotNone(correction.approved_at)


class SecurityIntegrationTest(TestCase):
    """セキュリティ統合テスト"""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@example.com", "pass123")
        self.department = Department.objects.create(name="総合診療科", code="GEN")
        self.position = Position.objects.create(
            name="事務職", code="ADMIN", department=self.department
        )

        self.employee = Employee.objects.create(
            user=self.user,
            employee_id="EMP001",
            first_name="従業員",
            last_name="太郎",
            department=self.department,
            position=self.position,
        )

    def test_rbac_permission_check(self):
        """RBAC権限チェックテスト"""
        from shifts.models.rbac import Role, Permission, UserRole, RBACMixin

        # 役割と権限作成
        role = Role.objects.create(name="一般職員", code="STAFF")
        permission = Permission.objects.create(
            name="シフト閲覧",
            code="view_shift",
            resource_type="shift",
            allowed_actions=["view"],
        )

        role.role_permissions.create(permission=permission)
        UserRole.objects.create(user=self.user, role=role)

        # 権限チェック
        has_permission = RBACMixin.check_permission(self.user, "shift", "view")
        self.assertTrue(has_permission)

        # 権限なしチェック
        has_no_permission = RBACMixin.check_permission(self.user, "shift", "delete")
        self.assertFalse(has_no_permission)

    def test_audit_log_creation(self):
        """監査ログ作成テスト"""
        from shifts.models.audit import AuditLog

        # API操作シミュレーション
        self.client.login(username="testuser", password="pass123")

        # シフト一覧閲覧
        response = self.client.get(reverse("shifts:shift-list"))

        # 監査ログ作成
        AuditLog.objects.create(
            user=self.user,
            action="VIEW",
            resource_type="Shift",
            resource_id=None,
            ip_address="127.0.0.1",
            user_agent="Test Browser",
            risk_level="LOW",
        )

        # ログ検証
        log = AuditLog.objects.filter(user=self.user).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, "VIEW")
        self.assertEqual(log.resource_type, "Shift")


@pytest.mark.django_db
class PerformanceIntegrationTest:
    """パフォーマンス統合テスト"""

    def test_bulk_shift_creation_performance(self):
        """大量シフト作成パフォーマンステスト"""
        from django.test.utils import override_settings
        from django.db import connection

        # テストデータ作成
        department = Department.objects.create(name="ICU", code="ICU")
        position = Position.objects.create(
            name="集中治療医", code="ICU_DOC", department=department
        )
        shift_type = ShiftType.objects.create(
            name="ICU夜勤", code="ICU_NIGHT", start_time="20:00", end_time="08:00"
        )

        # クエリ数測定
        with override_settings(DEBUG=True):
            initial_queries = len(connection.queries)

            # 30日分のシフト作成
            shifts = []
            base_date = timezone.now().date()

            for i in range(30):
                shift_date = base_date + timedelta(days=i)
                shifts.append(
                    Shift(
                        date=shift_date,
                        shift_type=shift_type,
                        department=department,
                        required_staff=3,
                    )
                )

            Shift.objects.bulk_create(shifts)

            final_queries = len(connection.queries)
            query_count = final_queries - initial_queries

            # クエリ数制限チェック（N+1問題回避）
            assert query_count <= 5, f"Too many queries: {query_count}"

            # 作成数検証
            assert Shift.objects.count() == 30

    def test_dashboard_performance(self):
        """ダッシュボードパフォーマンステスト"""
        import time

        # テストデータ大量作成
        department = Department.objects.create(name="救急科", code="ER")
        position = Position.objects.create(
            name="救急医", code="ER_DOC", department=department
        )

        # 100名の従業員作成
        employees = []
        for i in range(100):
            user = User.objects.create_user(f"user{i}", f"user{i}@hospital.com", "pass")
            employees.append(
                Employee(
                    user=user,
                    employee_id=f"EMP{i:03d}",
                    first_name=f"従業員{i}",
                    last_name="太郎",
                    department=department,
                    position=position,
                )
            )

        Employee.objects.bulk_create(employees)

        # ダッシュボード読み込み時間測定
        self.client.login(username="user0", password="pass")

        start_time = time.time()
        response = self.client.get(reverse("shifts:dashboard"))
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # ミリ秒

        # レスポンス時間制限
        assert response_time < 1000, f"Dashboard too slow: {response_time}ms"
        assert response.status_code == 200
