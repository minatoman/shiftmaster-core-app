from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Shift, ShiftRequest, ShiftType, Attendance, Notification


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'position', 'department', 'is_active', 'hire_date']
    list_filter = ['position', 'department', 'is_active', 'hire_date']
    search_fields = ['employee_id', 'name', 'user__username', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'employee_id', 'name', 'position', 'department')
        }),
        ('連絡先', {
            'fields': ('phone_number', 'email')
        }),
        ('その他', {
            'fields': ('hire_date', 'is_active', 'profile_image')
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ShiftType)
class ShiftTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'work_hours_display', 'color_preview', 'is_active']
    list_filter = ['is_active', 'start_time']
    search_fields = ['name']
    
    def work_hours_display(self, obj):
        return f"{obj.work_hours:.1f}時間"
    work_hours_display.short_description = '勤務時間'
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color_code
        )
    color_preview.short_description = '色'


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['employee', 'shift_date', 'shift_type', 'status', 'requested_by', 'approved_by']
    list_filter = ['status', 'shift_date', 'shift_type', 'employee__position']
    search_fields = ['employee__name', 'employee__employee_id']
    date_hierarchy = 'shift_date'
    raw_id_fields = ['employee', 'requested_by', 'approved_by']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('シフト情報', {
            'fields': ('employee', 'shift_date', 'shift_type', 'status')
        }),
        ('申請・承認', {
            'fields': ('requested_by', 'approved_by', 'notes')
        }),
        ('実績', {
            'fields': ('actual_start_time', 'actual_end_time', 'break_duration', 'overtime_hours')
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ShiftRequest)
class ShiftRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'request_type', 'original_shift', 'status', 'created_at']
    list_filter = ['request_type', 'status', 'created_at']
    search_fields = ['requester__name', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['requester', 'original_shift', 'swap_with_employee', 'reviewed_by']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['shift', 'check_in_time', 'check_out_time', 'total_work_time_display']
    list_filter = ['shift__shift_date', 'shift__employee__position']
    search_fields = ['shift__employee__name']
    readonly_fields = ['created_at', 'updated_at', 'total_work_time_display']
    
    def total_work_time_display(self, obj):
        total_time = obj.total_work_time
        if total_time:
            hours = int(total_time.total_seconds() // 3600)
            minutes = int((total_time.total_seconds() % 3600) // 60)
            return f"{hours}時間{minutes}分"
        return "未計算"
    total_work_time_display.short_description = '総労働時間'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__name', 'title', 'message']
    readonly_fields = ['created_at']
    raw_id_fields = ['recipient', 'related_shift', 'related_request']
