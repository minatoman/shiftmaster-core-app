# project_name/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

# Celeryの設定をDjangoの設定ファイルから読み込む
app.config_from_object('django.conf:settings', namespace='CELERY')

# タスクを自動的に登録
app.autodiscover_tasks()

