# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Shift
from datetime import timedelta

@shared_task
def send_alert(shift_id):
    shift = Shift.objects.get(id=shift_id)
    time_before_start = shift.shift_date - timedelta(minutes=10)
    if timezone.now() >= time_before_start:
        send_mail(
            'シフト開始10分前のアラート',
            f'{shift.employee.name}のシフトが10分後に開始します。',
            'from@example.com',
            [shift.employee.email],
            fail_silently=False,
        )

