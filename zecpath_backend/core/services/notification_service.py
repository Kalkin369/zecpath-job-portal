from django.core.mail import send_mail
from django.conf import settings

from core.models.notification_log import (
    NotificationLog
)
from core.services.email_templates import (
    application_status_template
)


def send_application_status_email(application):

    print("NOTIFICATION FUNCTION STARTED")

    candidate = application.candidate.user

    subject = "Application Status Updated"

    message = application_status_template(application)

    try:

        print("TRY BLOCK STARTED")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [candidate.email],
            fail_silently=False
        )

        print("EMAIL SENT SUCCESS")

        NotificationLog.objects.create(
            user=candidate,
            subject=subject,
            message=message,
            status='success'
        )

        print("LOG CREATED")

    except Exception as e:

        print("EMAIL ERROR:", str(e))

        NotificationLog.objects.create(
            user=candidate,
            subject=subject,
            message=message,
            status='failed',
            error_message=str(e)
        )