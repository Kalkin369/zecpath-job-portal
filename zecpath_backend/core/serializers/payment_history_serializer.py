from rest_framework import serializers

from core.models import PaymentTransaction


class PaymentHistorySerializer(serializers.ModelSerializer):

    plan = serializers.CharField(source="subscription.plan.name", read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "plan",
            "amount",
            "status",
            "gateway",
            "transaction_id",
            "created_at",
        ]
