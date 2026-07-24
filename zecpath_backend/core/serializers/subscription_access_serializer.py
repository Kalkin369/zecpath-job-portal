from rest_framework import serializers


class SubscriptionAccessSerializer(serializers.Serializer):

    subscription = serializers.CharField()

    active = serializers.BooleanField()

    ai_enabled = serializers.BooleanField()

    analytics_enabled = serializers.BooleanField()

    max_job_posts = serializers.IntegerField()

    jobs_used = serializers.IntegerField()

    jobs_remaining = serializers.IntegerField()

    max_candidate_access = serializers.IntegerField()

    candidate_access_used = serializers.IntegerField()

    candidate_access_remaining = serializers.IntegerField()

    start_date = serializers.DateField(
        allow_null=True
    )

    expires_on = serializers.DateField(
        allow_null=True
    )