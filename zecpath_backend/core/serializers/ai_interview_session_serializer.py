from rest_framework import serializers

from core.models.ai_interview_session import AIInterviewSession


class AIInterviewSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIInterviewSession
        fields = "__all__"
