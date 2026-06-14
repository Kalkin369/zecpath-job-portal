from django.db import models

from core.models.ai_answer import (AIAnswer)


class AnswerEvaluation(models.Model):

    answer = models.OneToOneField(AIAnswer,on_delete=models.CASCADE)

    relevance_score = models.FloatField(default=0)

    completeness_score = models.FloatField(default=0)

    keyword_score = models.FloatField(default=0)

    total_score = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Evaluation - {self.answer.id}")