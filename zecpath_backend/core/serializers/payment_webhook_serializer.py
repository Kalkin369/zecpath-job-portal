from rest_framework import serializers


class PaymentWebhookSerializer(serializers.Serializer):

    signature = serializers.CharField(required=True)
