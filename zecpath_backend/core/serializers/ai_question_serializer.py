from rest_framework import serializers

from core.models.ai_question import AIQuestion


class AIQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIQuestion
        fields = "__all__"
