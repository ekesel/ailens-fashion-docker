import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ailensfashion.settings')

app = Celery('ailensfashion')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()