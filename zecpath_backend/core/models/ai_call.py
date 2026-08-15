from django.db import models

from .application import Application


class AICall(models.Model):

    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    application = models.OneToOneField(Application, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")

    retry_count = models.IntegerField(default=0)

    scheduled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
