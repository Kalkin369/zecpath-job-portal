from rest_framework import serializers


class FinanceDashboardSerializer(serializers.Serializer):

    today_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    successful_transactions = serializers.IntegerField()

    failed_transactions = serializers.IntegerField()

    refunded_transactions = serializers.IntegerField()

    active_subscriptions = serializers.IntegerField()