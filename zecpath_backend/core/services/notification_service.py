from django.core.mail import send_mail
from django.conf import settings

def send_application_status_email(application):
    candidate_email = ( application.candidate.user.email)
    subject = "Application Status  Updated"
    message = (
        f"Your application for"
        f"{application.job.title}"
        f"is now {application.status}."
    )

    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[candidate_email],fail_silently=True)