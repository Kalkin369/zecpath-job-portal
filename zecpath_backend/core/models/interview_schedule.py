from django.db import models

from .application import Application


class InterviewSchedule(models.Model):

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    scheduled_at = models.DateTimeField()

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )

    created_at = models.DateTimeField(auto_now_add=True)
