from django.db import models
from core.models.ai_interview_session import (AIInterviewSession)
from core.models.question_template import (QuestionTemplate)

class AIQuestion(models.Model):

    session = models.ForeignKey( AIInterviewSession, on_delete=models.CASCADE,related_name='questions')

    template = models.ForeignKey(QuestionTemplate,on_delete=models.SET_NULL,null=True,blank=True)

    question_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )