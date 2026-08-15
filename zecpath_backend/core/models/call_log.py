from django.db import models

from .ai_call import AICall


class CallLog(models.Model):

    ai_call = models.ForeignKey(AICall, on_delete=models.CASCADE)

    event = models.CharField(max_length=255)

    triggered_by = models.CharField(max_length=100)

    reason = models.CharField(max_length=225)

    created_at = models.DateTimeField(auto_now_add=True)
