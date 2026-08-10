from rest_framework import serializers


class MonthlyRevenueSerializer(serializers.Serializer):

    month = serializers.SerializerMethodField()

    revenue = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transactions = serializers.IntegerField()

    def get_month(self,obj) -> str:
        return obj["month"].date()