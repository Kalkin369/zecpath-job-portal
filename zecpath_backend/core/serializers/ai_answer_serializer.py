from rest_framework import serializers

from core.models.ai_answer import AIAnswer


class AIAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAnswer
        fields = "__all__"
