from django.db import models

from core.models import (
    Application
)


class CandidateReport(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE
    )

    ats_score = models.FloatField(
        default=0
    )

    ai_score = models.FloatField(
        default=0
    )

    strengths = models.JSONField(
        default=list
    )

    risks = models.JSONField(
        default=list
    )

    summary = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )