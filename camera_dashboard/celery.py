from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from jobs import feeds, sync_agents

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camera_dashboard.settings')
app = Celery('camera_dashboard')
app.conf.broker_url = 'amqp://rabbitmq'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/7 * * * *"), sync_agents.do_sync())
    sender.add_periodic_task(crontab(minute="*/5 * * * *"), feeds.get_feeds())
