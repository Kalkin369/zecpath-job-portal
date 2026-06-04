from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','zecpath_backend.settings')

app = Celery('zecpath_backend')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()