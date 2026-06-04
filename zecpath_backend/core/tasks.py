from celery import shared_task

from core.models.application import Application
from core.services.notification_service import (send_application_status_email)

@shared_task
def test_task():

    print("Celery Working")

    return "Success"
@shared_task
def send_status_email_task(application_id):

    application = Application.objects.get(id=application_id)
    
    send_application_status_email(application)










