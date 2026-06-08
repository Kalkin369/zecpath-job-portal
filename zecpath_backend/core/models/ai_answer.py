from django.db import models
from core.models.ai_question import (
    AIQuestion
)


class AIAnswer(models.Model):

    question = models.OneToOneField(
        AIQuestion,
        on_delete=models.CASCADE
    )

    answer_text = models.TextField()

    score = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )