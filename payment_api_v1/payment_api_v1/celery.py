import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_api_v1.settings')

app = Celery('payment_api_v1')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
