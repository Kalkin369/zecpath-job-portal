from django.db import models

from core.models.ai_interview_session import (
    AIInterviewSession
)


class InterviewState(models.Model):

    session = models.OneToOneField(AIInterviewSession,on_delete=models.CASCADE)

    current_question_index = models.IntegerField( default=0)

    current_category = models.CharField(max_length=50,blank=True)

    is_completed = models.BooleanField(default=False)