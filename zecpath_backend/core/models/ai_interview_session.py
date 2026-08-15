from django.db import models

from .ai_call import AICall


class AIInterviewSession(models.Model):

    ai_call = models.OneToOneField(AICall, on_delete=models.CASCADE)

    started_at = models.DateTimeField(auto_now_add=True)

    ended_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, default="in_progress")

    transcript = models.JSONField(null=True, blank=True)
