from celery import shared_task

from core.models.application import Application
from core.services.notification_service import (send_application_status_email)
from core.models import (InterviewSchedule)

@shared_task
def test_task():

    print("Celery Working")

    return "Success"
@shared_task
def send_status_email_task(application_id):

    application = Application.objects.get(id=application_id)
    
    send_application_status_email(application)

@shared_task
def send_schedule_email_task(schedule_id):

    try:

        schedule = (InterviewSchedule.objects.get(id=schedule_id))

        application = (schedule.application)

        print(
            f"Interview Scheduled for "
            f"{application.id} at "
            f"{schedule.scheduled_at}"
        )

        return {"status": "success"}

    except Exception as e:

        return {"status": "failed","error": str(e)}








