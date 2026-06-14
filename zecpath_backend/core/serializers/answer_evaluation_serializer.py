from rest_framework import serializers

from core.models.answer_evaluation import (AnswerEvaluation)


class AnswerEvaluationSerializer(serializers.ModelSerializer):

    class Meta:

        model = AnswerEvaluation

        fields = '__all__'