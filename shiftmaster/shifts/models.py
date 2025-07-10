from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Employee(models.Model):
    """従業員モデル"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    employee_id = models.CharField(max_length=20, unique=True, verbose_name='従業員ID')
    name = models.CharField(max_length=100, verbose_name='氏名')
    position = models.CharField(max_length=100, verbose_name='職種')
    department = models.CharField(max_length=100, verbose_name='部署', blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='電話番号', blank=True)
    email = models.EmailField(verbose_name='メールアドレス', blank=True)
    hire_date = models.DateField(verbose_name='入社日', default=timezone.now)
    is_active = models.BooleanField(default=True, verbose_name='アクティブ')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='プロフィール画像')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '従業員'
        verbose_name_plural = '従業員'
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.employee_id} - {self.name}"


class ShiftType(models.Model):
    """シフトタイプモデル"""
    name = models.CharField(max_length=50, unique=True, verbose_name='シフト名')
    start_time = models.TimeField(verbose_name='開始時間')
    end_time = models.TimeField(verbose_name='終了時間')
    break_time = models.DurationField(verbose_name='休憩時間', default=timezone.timedelta(hours=1))
    color_code = models.CharField(max_length=7, default='#007bff', verbose_name='表示色')
    is_active = models.BooleanField(default=True, verbose_name='アクティブ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'シフトタイプ'
        verbose_name_plural = 'シフトタイプ'
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time}-{self.end_time})"

    @property
    def work_hours(self):
        """実働時間を計算"""
        from datetime import datetime, timedelta
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        if end < start:  # 日をまたぐ場合
            end += timedelta(days=1)
        work_duration = end - start - self.break_time
        return work_duration.total_seconds() / 3600  # 時間で返す


class Shift(models.Model):
    """シフトモデル"""
    SHIFT_STATUS_CHOICES = [
        ('pending', '申請中'),
        ('approved', '承認済み'),
        ('rejected', '却下'),
        ('completed', '完了'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shifts', verbose_name='従業員')
    shift_date = models.DateField(verbose_name='シフト日')
    shift_type = models.ForeignKey(ShiftType, on_delete=models.CASCADE, verbose_name='シフトタイプ')
    status = models.CharField(max_length=10, choices=SHIFT_STATUS_CHOICES, default='pending', verbose_name='ステータス')
    requested_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='requested_shifts', verbose_name='申請者')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='approved_shifts', verbose_name='承認者')
    notes = models.TextField(blank=True, verbose_name='備考')
    actual_start_time = models.TimeField(null=True, blank=True, verbose_name='実際の開始時間')
    actual_end_time = models.TimeField(null=True, blank=True, verbose_name='実際の終了時間')
    break_duration = models.DurationField(null=True, blank=True, verbose_name='実際の休憩時間')
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='残業時間')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'シフト'
        verbose_name_plural = 'シフト'
        unique_together = ['employee', 'shift_date']
        ordering = ['-shift_date', 'employee__employee_id']

    def __str__(self):
        return f"{self.employee.name} - {self.shift_date} ({self.shift_type.name})"

    @property
    def actual_work_hours(self):
        """実際の労働時間を計算"""
        if self.actual_start_time and self.actual_end_time:
            from datetime import datetime, timedelta
            start = datetime.combine(self.shift_date, self.actual_start_time)
            end = datetime.combine(self.shift_date, self.actual_end_time)
            if end < start:  # 日をまたぐ場合
                end += timedelta(days=1)
            break_time = self.break_duration or self.shift_type.break_time
            work_duration = end - start - break_time
            return work_duration.total_seconds() / 3600
        return self.shift_type.work_hours


class ShiftRequest(models.Model):
    """シフト変更申請モデル"""
    REQUEST_TYPE_CHOICES = [
        ('change', 'シフト変更'),
        ('swap', 'シフト交換'),
        ('cancel', 'シフト取消'),
        ('overtime', '残業申請'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shift_requests', verbose_name='申請者')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES, verbose_name='申請タイプ')
    original_shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='change_requests', verbose_name='元のシフト')
    new_shift_type = models.ForeignKey(ShiftType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='新しいシフトタイプ')
    swap_with_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='swap_requests', verbose_name='交換相手')
    reason = models.TextField(verbose_name='理由')
    status = models.CharField(max_length=10, choices=Shift.SHIFT_STATUS_CHOICES, default='pending', verbose_name='ステータス')
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='reviewed_requests', verbose_name='承認者')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='承認日時')
    admin_notes = models.TextField(blank=True, verbose_name='管理者メモ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'シフト申請'
        verbose_name_plural = 'シフト申請'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requester.name} - {self.get_request_type_display()} ({self.original_shift.shift_date})"


class Attendance(models.Model):
    """出勤記録モデル"""
    shift = models.OneToOneField(Shift, on_delete=models.CASCADE, related_name='attendance', verbose_name='シフト')
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name='チェックイン時間')
    check_out_time = models.DateTimeField(null=True, blank=True, verbose_name='チェックアウト時間')
    break_start_time = models.DateTimeField(null=True, blank=True, verbose_name='休憩開始時間')
    break_end_time = models.DateTimeField(null=True, blank=True, verbose_name='休憩終了時間')
    location = models.CharField(max_length=200, blank=True, verbose_name='勤務場所')
    notes = models.TextField(blank=True, verbose_name='備考')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '出勤記録'
        verbose_name_plural = '出勤記録'

    def __str__(self):
        return f"{self.shift.employee.name} - {self.shift.shift_date}"

    @property
    def total_work_time(self):
        """総労働時間を計算"""
        if self.check_in_time and self.check_out_time:
            work_time = self.check_out_time - self.check_in_time
            if self.break_start_time and self.break_end_time:
                break_time = self.break_end_time - self.break_start_time
                work_time -= break_time
            return work_time
        return None


class Notification(models.Model):
    """通知モデル"""
    NOTIFICATION_TYPE_CHOICES = [
        ('shift_assigned', 'シフト割当'),
        ('shift_changed', 'シフト変更'),
        ('request_approved', '申請承認'),
        ('request_rejected', '申請却下'),
        ('reminder', 'リマインダー'),
        ('announcement', 'お知らせ'),
    ]

    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications', verbose_name='受信者')
    title = models.CharField(max_length=200, verbose_name='タイトル')
    message = models.TextField(verbose_name='メッセージ')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='通知タイプ')
    is_read = models.BooleanField(default=False, verbose_name='既読')
    related_shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True, blank=True, verbose_name='関連シフト')
    related_request = models.ForeignKey(ShiftRequest, on_delete=models.CASCADE, null=True, blank=True, verbose_name='関連申請')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.name} - {self.title}"
