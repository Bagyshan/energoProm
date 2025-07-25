from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Добавить поддержку celery beat
from celery.schedules import crontab
from django.conf import settings

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'