# project_name/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Djangoの設定モジュールを設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

# Celeryアプリケーションのインスタンス化
app = Celery('project_name')

# 設定の読み込み
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動的にDjangoのtasks.pyを読み込む
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
