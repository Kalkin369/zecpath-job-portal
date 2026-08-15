from django.conf import settings
from django.core.mail import send_mail

from core.models.notification_log import NotificationLog
from core.services.email_templates import (application_status_template,
                                           payment_failed_template,
                                           payment_success_template,
                                           refund_processed_template)


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
            fail_silently=False,
        )

        print("EMAIL SENT SUCCESS")

        NotificationLog.objects.create(
            user=candidate, subject=subject, message=message, status="success"
        )

        print("LOG CREATED")

    except Exception as e:

        print("EMAIL ERROR:", str(e))

        NotificationLog.objects.create(
            user=candidate,
            subject=subject,
            message=message,
            status="failed",
            error_message=str(e),
        )


def send_payment_success_email(payment):

    employer = payment.subscription.employer.user

    subject = "Payment Successful"

    message = payment_success_template(payment)

    try:

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [employer.email],
            fail_silently=False,
        )

        NotificationLog.objects.create(
            user=employer, subject=subject, message=message, status="success"
        )

    except Exception as e:

        NotificationLog.objects.create(
            user=employer,
            subject=subject,
            message=message,
            status="failed",
            error_message=str(e),
        )


def send_payment_failed_email(payment):

    employer = payment.subscription.employer.user

    subject = "Payment Failed"

    message = payment_failed_template(payment)

    try:

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [employer.email],
            fail_silently=False,
        )

        NotificationLog.objects.create(
            user=employer, subject=subject, message=message, status="success"
        )

    except Exception as e:

        NotificationLog.objects.create(
            user=employer,
            subject=subject,
            message=message,
            status="failed",
            error_message=str(e),
        )


def send_refund_processed_email(payment):

    employer = payment.subscription.employer.user

    subject = "Refund Processed"

    message = refund_processed_template(payment)

    try:

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [employer.email],
            fail_silently=False,
        )

        NotificationLog.objects.create(
            user=employer, subject=subject, message=message, status="success"
        )

    except Exception as e:

        NotificationLog.objects.create(
            user=employer,
            subject=subject,
            message=message,
            status="failed",
            error_message=str(e),
        )
