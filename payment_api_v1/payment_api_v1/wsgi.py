import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_api_v1.settings')

application = get_wsgi_application()
