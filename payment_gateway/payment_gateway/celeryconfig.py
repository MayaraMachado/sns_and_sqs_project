from django.conf import settings
from datetime import timedelta

CELERY_APPS = [
    'api',
]


BROKER_URL = 'redis://redis:6379/10'
CELERY_RESULT_BACKEND = 'redis://redis:6379/10'
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = settings.TIME_ZONE
