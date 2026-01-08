# alx_travel_app_0x03
## Duplicate the Project
Duplicate:
alx_travel_app_0x02
to:
alx_travel_app_0x03

### Install Required Packages
pip install celery django-celery-results

#### Create celery.py (Project Root)
alx_travel_app_0x03/
 ├── alx_travel_app/
 │   ├── __init__.py
 │   ├── settings.py
 │   ├── celery.py   

 import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

##### Update __init__.py
from .celery import app as celery_app
__all__ = ('celery_app',)

###### Configure Celery in settings.py
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

If using results (optional but recommended):
INSTALLED_APPS += ['django_celery_results']
CELERY_RESULT_BACKEND = 'django-db'

Then run:
python manage.py migrate

###### Configure Django Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

###### Define Email Task (listings/tasks.py)
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(email, booking_id):
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been confirmed."
    send_mail(
        subject,
        message,
        None,
        [email],
        fail_silently=False,
    )

###### Trigger Email Task in BookingViewSet
from listings.tasks import send_booking_confirmation_email

def perform_create(self, serializer):
    booking = serializer.save()
    send_booking_confirmation_email.delay(
        booking.user.email,
        booking.id
    )

###### Run and Test Background Task
sudo service rabbitmq-server start

Start Celery Worker
celery -A alx_travel_app worker -l info
