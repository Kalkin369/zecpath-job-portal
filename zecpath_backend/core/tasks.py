from celery import shared_task

from core.models.application import Application
from core.services.notification_service import (send_application_status_email)
from core.models import (InterviewSchedule)
from core.services.reminder_service import ReminderService
from django.utils import timezone
from core.services.reminder_message_service import (ReminderMessageService)

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

@shared_task
def send_interview_reminder_task():

    reminders = (
        ReminderService().get_pending_reminders())

    for reminder in reminders:

        try:

            message = (ReminderMessageService().build_email(reminder.schedule))

            print(message)

            reminder.status = 'sent'

            reminder.sent_at = (timezone.now())

            reminder.save()

        except Exception as e:

            print(f"Reminder failed: {e}")

            reminder.status = ('failed')

            reminder.save()        








