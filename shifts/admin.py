from django.contrib import admin
from .models import (
    Employee, Shift, ShiftRequest, HolidayRequest, LeaveBalance, 
    Committee, OnCallShift, ShiftRequirement, ShiftLog, NotificationLog
)
from .utils import normalize_name

# ✅ 氏名一括正規化アクション
@admin.action(description="氏名の空白を正規化")
def normalize_employee_names(modeladmin, request, queryset):
    updated = 0
    for emp in queryset:
        normalized = normalize_name(emp.name)
        if emp.name != normalized:
            emp.name = normalized
            emp.save()
            updated += 1
    modeladmin.message_user(request, f"{updated} 件の氏名を正規化しました。")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'position', 'department', 'employment_type',
        'hire_date', 'is_active'
    )
    search_fields = ('name', 'email', 'position', 'department')
    list_filter = ('position', 'department', 'employment_type', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    actions = [normalize_employee_names]


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'shift_date', 'shift_type', 'is_approved', 'approved_at')
    search_fields = ('employee__name', 'shift_date')
    list_filter = ('shift_type', 'is_approved', 'shift_date')
    list_editable = ('is_approved',)


@admin.register(ShiftRequest)
class ShiftRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'requested_date', 'shift_type', 'priority', 'approved', 'created_at')
    list_filter = ('approved', 'shift_type', 'created_at')
    search_fields = ('employee__name',)


@admin.register(HolidayRequest)
class HolidayRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'holiday_date', 'holiday_type', 'request_date')
    list_filter = ('holiday_type', 'request_date')
    search_fields = ('employee__name',)


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'annual_leave', 'compensatory_leave', 'weekend_leave', 'night_shift_leave')
    search_fields = ('employee__name',)
    list_filter = ('employee',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + (
                'annual_leave', 'compensatory_leave', 'weekend_leave', 'night_shift_leave'
            )
        return self.readonly_fields


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule_type', 'weekday', 'day_of_month', 'time', 'description')
    search_fields = ('name',)
    list_filter = ('schedule_type',)


@admin.register(OnCallShift)
class OnCallShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'shift_type', 'start_datetime', 'end_datetime')
    search_fields = ('employee__name',)
    list_filter = ('shift_type',)


@admin.register(ShiftRequirement)
class ShiftRequirementAdmin(admin.ModelAdmin):
    list_display = (
        'day_of_week',
        'nurse_required',
        'engineer_required',
        'assistant_required',
        'total_required',
        'note'
    )
    list_editable = (
        'nurse_required',
        'engineer_required',
        'assistant_required',
        'total_required',
    )


@admin.register(ShiftLog)
class ShiftLogAdmin(admin.ModelAdmin):
    list_display = ('shift', 'action', 'timestamp', 'performed_by')
    search_fields = ('shift__employee__name', 'shift__shift_date', 'performed_by__username')
    list_filter = ('action', 'timestamp')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sent_at', 'method')
    search_fields = ('recipient', 'method')
    list_filter = ('method',)

