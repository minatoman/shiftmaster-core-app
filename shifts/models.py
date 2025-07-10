from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# === スタッフ情報モデル（完全版） ===
class Employee(models.Model):
    name = models.CharField(max_length=100)
    name_kana = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    department = models.CharField(max_length=100)
    assigned_locations = models.JSONField(blank=True, null=True)
    position = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=50, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    work_constraints = models.JSONField(blank=True, null=True)
    qualifications = models.JSONField(blank=True, null=True)
    work_details = models.JSONField()  # null不可
    committees = models.JSONField(blank=True, null=True)
    teams = models.JSONField(blank=True, null=True)
    clinical_ladder = models.CharField(max_length=10, blank=True, null=True)
    yearly_goals = models.TextField(blank=True, null=True)
    career_history = models.TextField(blank=True, null=True)

    ability_rating = models.JSONField(blank=True, null=True)
    performance_evaluation = models.JSONField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    interview_history = models.JSONField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # ✅ LINE通知用トークン（通知機能対応）
    line_notify_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


# === 休暇残数モデル ===
class LeaveBalance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='leave_balance')
    annual_leave = models.FloatField(default=0)
    compensatory_leave = models.FloatField(default=0)
    weekend_leave = models.FloatField(default=0)
    night_shift_leave = models.FloatField(default=0)
    max_annual_leave = models.FloatField(default=40)
    goal_annual_leave = models.FloatField(default=20)
    admin_only = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.employee.name}の休暇残数'

    def update_leave(self, leave_type, amount):
        if leave_type == 'annual_leave':
            self.annual_leave = min(self.annual_leave + amount, self.max_annual_leave)
        elif leave_type == 'compensatory_leave':
            self.compensatory_leave += amount
        elif leave_type == 'weekend_leave':
            self.weekend_leave += amount
        elif leave_type == 'night_shift_leave':
            self.night_shift_leave += amount
        self.save()

    def goal_met(self):
        return self.annual_leave >= self.goal_annual_leave

    def reset_annual_leave(self):
        self.annual_leave = 20
        self.save()


# === シフトモデル ===
class Shift(models.Model):
    SHIFT_TYPES = [
        ('morning', '午前'),
        ('afternoon', '午後'),
        ('night', '夜勤'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift_date = models.DateField()
    shift_type = models.CharField(max_length=50, choices=SHIFT_TYPES, default='morning')
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.shift_date} ({self.get_shift_type_display()})"

# === 勤務希望モデル ===
class ShiftRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    requested_date = models.DateField()
    shift_type = models.CharField(max_length=50, choices=Shift.SHIFT_TYPES)
    priority = models.IntegerField(default=1)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.requested_date} ({self.shift_type})"

    def is_editable(self):
        return timezone.now().day <= 17


# === シフトログ ===
class ShiftLog(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


# === 休暇申請モデル ===
class HolidayRequest(models.Model):
    HOLIDAY_TYPES = [
        ('paid', '有給休暇'),
        ('substitute', '振替休暇'),
        ('weekend', '週末休暇'),
        ('summer', '夏季休暇'),
        ('special', '特別休暇'),
        ('exemption', '免除休暇'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    holiday_date = models.DateField()
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPES)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.holiday_date} ({self.get_holiday_type_display()})"


# === 委員会スケジュール ===
class Committee(models.Model):
    name = models.CharField(max_length=100)
    schedule_type = models.CharField(max_length=50, choices=[
        ('weekly', '週次'),
        ('monthly', '月次'),
        ('ad_hoc', '臨時'),
    ])
    weekday = models.CharField(max_length=10, blank=True, null=True)
    day_of_month = models.IntegerField(blank=True, null=True)
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.schedule_type})'


# === 夜間呼出シフト ===
class OnCallShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    shift_type = models.CharField(max_length=50, choices=[
        ('night', '夜間呼出'),
        ('weekend', '週末呼出'),
    ])

    def __str__(self):
        return f'{self.employee.name} ({self.shift_type}) - {self.start_datetime} → {self.end_datetime}'


# === シフト要件モデル ===
class ShiftRequirement(models.Model):
    DAY_CHOICES = [
        ('Monday', '月曜日'),
        ('Tuesday', '火曜日'),
        ('Wednesday', '水曜日'),
        ('Thursday', '木曜日'),
        ('Friday', '金曜日'),
        ('Saturday', '土曜日'),
        ('Sunday', '日曜日'),
    ]
    
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    nurse_required = models.IntegerField(default=0, verbose_name='看護師必要人数')
    engineer_required = models.IntegerField(default=0, verbose_name='臨床工学技士必要人数')
    assistant_required = models.IntegerField(default=0, verbose_name='看護補助必要人数')
    total_required = models.IntegerField(default=0, verbose_name='必要合計人数')
    note = models.TextField(blank=True, null=True, verbose_name='備考')

    def __str__(self):
        return f"{self.get_day_of_week_display()}: 看護師{self.nurse_required}名, 工学技士{self.engineer_required}名, 補助{self.assistant_required}名"

    class Meta:
        verbose_name = 'シフト要件'
        verbose_name_plural = 'シフト要件'


# === 通知ログモデル（LINE・メール共通） ===
class NotificationLog(models.Model):
    recipient = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=(('email', 'メール'), ('line', 'LINE')))


# === プロフィールモデル（ユーザー追加情報） ===
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# === 透析患者モデル ===
class DialysisPatient(models.Model):
    name = models.CharField(max_length=50)
    dialysis_time = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    area = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.name}"


# === 透析記録：勤務者登録 ===
class DialysisStaff(models.Model):
    name = models.CharField(max_length=50)
    shift_type = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    remarks_am = models.CharField(max_length=100, blank=True, null=True)
    remarks_pm = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.name}"

