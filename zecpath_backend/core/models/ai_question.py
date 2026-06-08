from django.db import models
from core.models.ai_interview_session import (
    AIInterviewSession
)


class AIQuestion(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )