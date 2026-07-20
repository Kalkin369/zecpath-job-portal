from rest_framework import serializers


class RefundPaymentSerializer(serializers.Serializer):

    payment_id = serializers.IntegerField()

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )