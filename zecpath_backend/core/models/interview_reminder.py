from django.db import models

from .interview_schedule import InterviewSchedule


class InterviewReminder(models.Model):

    STATUS_CHOICES = [("pending", "Pending"), ("sent", "Sent"), ("failed", "Failed")]

    schedule = models.ForeignKey(
        InterviewSchedule, on_delete=models.CASCADE, related_name="reminders"
    )

    reminder_type = models.CharField(max_length=50)

    scheduled_for = models.DateTimeField()

    sent_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
