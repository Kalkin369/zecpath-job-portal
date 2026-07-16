from rest_framework.serializers import ModelSerializer

from core.models import PaymentTransaction


class PaymentTransactionSerializer(ModelSerializer):

    class Meta:

        model = PaymentTransaction

        fields = "__all__"