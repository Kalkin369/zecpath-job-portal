from rest_framework import serializers


class HiringEfficiencySerializer(serializers.Serializer):

    total_jobs = serializers.IntegerField()

    total_applications = serializers.IntegerField()

    selected_candidates = serializers.IntegerField()

    average_ats_score = serializers.FloatField()

    average_ai_score = serializers.FloatField()

    hiring_success_rate = serializers.FloatField()
