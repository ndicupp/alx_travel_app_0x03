alx_travel_app_0x02
alx_travel_app_0x03

pip install celery django-celery-results

#celery.py

alx_travel_app_0x03/
 ├── alx_travel_app/
 │   ├── __init__.py
 │   ├── settings.py
 │   ├── celery.py   

import os
from celery import Celery

# Set default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')

# Load task modules from all registered Django apps.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

#alx_travel_app/__init__.py

from .celery import app as celery_app
__all__ = ('celery_app',)

#settings.py

# Celery Configuration
CELERY_BROKER_URL = 'amqp://localhost'  # Default RabbitMQ port
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

INSTALLED_APPS += ['django_celery_results']
CELERY_RESULT_BACKEND = 'django-db'

python manage.py migrate


#settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#listings/tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    subject = 'Booking Confirmation'
    message = f'Your booking for {booking_details} has been confirmed!'
    recipient_list = [user_email]
    send_mail(subject, message, 'admin@alxtravel.com', recipient_list)

#BookingViewSet

class BookingViewSet(viewsets.ModelViewSet):
    # ... your existing code ...

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger the background task
        send_booking_confirmation_email.delay(booking.user.email, str(booking))


sudo service rabbitmq-server start

celery -A alx_travel_app worker -l info





   
