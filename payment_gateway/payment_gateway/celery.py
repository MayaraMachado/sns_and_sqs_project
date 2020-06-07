from __future__ import absolute_import
import os
from celery.schedules import crontab
from . import celeryconfig
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payment_gateway.settings")
app = Celery('payment_gateway')
app.config_from_object(celeryconfig)
app.autodiscover_tasks(lambda: celeryconfig.CELERY_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
