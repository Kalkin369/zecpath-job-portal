from rest_framework import serializers


class CandidateRankingSerializer(serializers.Serializer):

    candidate = serializers.CharField()

    job = serializers.CharField()

    ats_score = serializers.FloatField()

    ai_score = serializers.FloatField()

    final_score = serializers.FloatField()

    status = serializers.CharField()