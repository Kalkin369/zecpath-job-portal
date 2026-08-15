from rest_framework import serializers


class CreatePaymentOrderSerializer(serializers.Serializer):

    subscription_id = serializers.IntegerField()
