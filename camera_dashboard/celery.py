from __future__ import absolute_import
import os
from celery import Celery
import django
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camera_dashboard.settings')
django.setup()
app = Celery('camera_dashboard')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)

app.conf.beat_schedule = {
    'do_sync': {
        'task': 'jobs.sync_agents.do_sync',
        'schedule': crontab(minute="3", hour="0")
    },
    'get_feeds': {
        'task': 'jobs.feeds.get_feeds',
        'schedule': crontab(minute="*/5 * * * *")
    },
}
