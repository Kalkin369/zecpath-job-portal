from rest_framework import serializers


class CandidatePredictionSerializer(serializers.Serializer):

    candidate = serializers.CharField()

    job = serializers.CharField()

    ats_score = serializers.FloatField()

    ai_score = serializers.FloatField()

    prediction = serializers.CharField()