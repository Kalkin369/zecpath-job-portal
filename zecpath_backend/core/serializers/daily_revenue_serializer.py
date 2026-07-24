from rest_framework import serializers


class DailyRevenueSerializer(serializers.Serializer):

    day = serializers.DateField()

    revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transactions = serializers.IntegerField()