from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims.settings')

app = Celery('ims')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_due_reminders_every_morning': {
        'task': 'inventory.tasks.send_reminder_emails',
        'schedule': crontab(hour=14, minute=46), 
    },
}
