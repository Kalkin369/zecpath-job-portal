from rest_framework import serializers


class PaymentFailureSerializer(serializers.Serializer):

    payment_id = serializers.IntegerField()

    employer = serializers.CharField()

    plan = serializers.CharField()

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    gateway = serializers.CharField()

    status = serializers.CharField()

    created_at = serializers.DateTimeField()