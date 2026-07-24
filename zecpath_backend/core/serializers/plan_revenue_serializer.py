from rest_framework import serializers


class PlanRevenueSerializer(serializers.Serializer):

    plan_name = serializers.CharField()

    revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    subscriptions = serializers.IntegerField()