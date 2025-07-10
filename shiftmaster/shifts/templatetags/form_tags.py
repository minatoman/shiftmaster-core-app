from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import calendar
from datetime import date, timedelta

register = template.Library()


@register.filter
def add_css_class(field, css_class):
    """フォームフィールドにCSSクラスを追加"""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field


@register.filter
def add_class(field, css_class):
    """フォームフィールドにCSSクラスを追加（エイリアス）"""
    return add_css_class(field, css_class)


@register.filter
def bootstrap_form_field(field):
    """Bootstrap用のフォームフィールドレンダリング"""
    css_class = 'form-control'
    if field.field.widget.__class__.__name__ == 'CheckboxInput':
        css_class = 'form-check-input'
    elif field.field.widget.__class__.__name__ == 'RadioSelect':
        css_class = 'form-check-input'
    
    return field.as_widget(attrs={'class': css_class})


@register.simple_tag
def shift_color_indicator(shift_type):
    """シフトタイプの色インジケーターを表示"""
    return format_html(
        '<span class="badge" style="background-color: {}">{}</span>',
        shift_type.color_code,
        shift_type.name
    )


@register.filter
def status_badge(status):
    """ステータスバッジを表示"""
    status_classes = {
        'pending': 'bg-warning text-dark',
        'approved': 'bg-success',
        'rejected': 'bg-danger',
        'completed': 'bg-info',
    }
    
    status_labels = {
        'pending': '申請中',
        'approved': '承認済み',
        'rejected': '却下',
        'completed': '完了',
    }
    
    css_class = status_classes.get(status, 'bg-secondary')
    label = status_labels.get(status, status)
    
    return format_html(
        '<span class="badge {}">{}</span>',
        css_class,
        label
    )


@register.filter
def weekday_name(date_obj):
    """日本語の曜日名を返す"""
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    return weekdays[date_obj.weekday()]


@register.simple_tag
def calendar_month_name(month_num):
    """月名を日本語で返す"""
    month_names = [
        '', '1月', '2月', '3月', '4月', '5月', '6月',
        '7月', '8月', '9月', '10月', '11月', '12月'
    ]
    return month_names[month_num]


@register.filter
def duration_hours(duration):
    """DurationFieldを時間で表示"""
    if duration:
        total_seconds = duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}時間{minutes}分"
    return "未設定"


@register.filter
def mobile_truncate(text, length=20):
    """モバイル用の文字列切り詰め"""
    if len(text) <= length:
        return text
    return text[:length] + '...'


@register.simple_tag
def attendance_status_icon(attendance):
    """出勤状況のアイコンを表示"""
    if not attendance:
        return format_html('<i class="bi bi-circle text-muted"></i>')
    
    if attendance.check_out_time:
        return format_html(
            '<i class="bi bi-check-circle-fill text-success"></i>'
        )
    elif attendance.break_start_time and not attendance.break_end_time:
        return format_html(
            '<i class="bi bi-pause-circle-fill text-warning"></i>'
        )
    elif attendance.check_in_time:
        return format_html('<i class="bi bi-play-circle-fill text-info"></i>')
    else:
        return format_html('<i class="bi bi-circle text-muted"></i>')


@register.filter
def notification_icon(notification_type):
    """通知タイプのアイコンを返す"""
    icons = {
        'shift_assigned': 'bi-calendar-plus',
        'shift_changed': 'bi-calendar-event',
        'request_approved': 'bi-check-circle',
        'request_rejected': 'bi-x-circle',
        'reminder': 'bi-alarm',
        'announcement': 'bi-megaphone',
    }
    return icons.get(notification_type, 'bi-info-circle')


@register.simple_tag
def range_dates(start_date, end_date):
    """日付範囲のリストを生成"""
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


@register.filter
def is_today(date_obj):
    """今日かどうかを判定"""
    return date_obj == date.today()


@register.filter
def is_weekend(date_obj):
    """週末かどうかを判定（土日）"""
    return date_obj.weekday() in [5, 6]


@register.simple_tag(takes_context=True)
def mobile_device(context):
    """モバイルデバイスかどうかを判定"""
    request = context['request']
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = [
        'mobile', 'android', 'iphone', 'ipad', 'blackberry', 'webos'
    ]
    return any(keyword in user_agent for keyword in mobile_keywords)


@register.inclusion_tag('shifts/components/shift_card.html')
def shift_card(shift, show_employee=True):
    """シフトカードコンポーネント"""
    return {
        'shift': shift,
        'show_employee': show_employee,
    }


@register.inclusion_tag('shifts/components/notification_item.html')
def notification_item(notification):
    """通知アイテムコンポーネント"""
    return {
        'notification': notification,
    }
