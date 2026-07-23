from celery import shared_task

from core.models.application import Application
from core.services.notification_service import (send_application_status_email,send_payment_success_email,
                                                send_payment_failed_email,send_refund_processed_email,
)
from core.models import (InterviewSchedule,PaymentTransaction)
from core.services.reminder_service import ReminderService
from django.utils import timezone
from core.services.reminder_message_service import (ReminderMessageService)
from core.services.logging_service import (LoggingService)
from core.services.subscription_service import (SubscriptionService)

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
    
    print(f"Found {reminders.count()} reminders")

    for reminder in reminders:

        try:

            message = (ReminderMessageService().build_email(reminder.schedule))

            print(message)

           
            reminder.status = 'sent'

            reminder.sent_at = (timezone.now())

            reminder.save()

        except Exception as e:

            print(f"Reminder failed: {e}")

            LoggingService().create_error_log(
                "send_interview_reminder_task",f"Reminder {reminder.id}:{str(e)}"
            )

            reminder.status = ('failed')

            reminder.save() 

@shared_task
def send_payment_success_email_task(payment_id):

    payment = PaymentTransaction.objects.select_related(
        "subscription",
        "subscription__plan",
        "subscription__employer__user",
    ).get(id=payment_id)

    send_payment_success_email(payment)


@shared_task
def send_payment_failed_email_task(payment_id):

    payment = PaymentTransaction.objects.select_related(
        "subscription",
        "subscription__plan",
        "subscription__employer__user",
    ).get(id=payment_id)

    send_payment_failed_email(payment)


@shared_task
def send_refund_processed_email_task(payment_id):

    payment = PaymentTransaction.objects.select_related(
        "subscription",
        "subscription__plan",
        "subscription__employer__user",
    ).get(id=payment_id)

    send_refund_processed_email(payment)                   



@shared_task
def deactivate_expired_subscriptions():

    updated_count = (
        SubscriptionService()
        .deactivate_all_expired_subscriptions()
    )

    return (
        f"{updated_count} expired subscriptions deactivated."
    )







