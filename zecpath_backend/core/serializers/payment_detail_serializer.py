from rest_framework import serializers
from core.models import PaymentTransaction


class PaymentDetailSerializer(serializers.ModelSerializer):

    plan = serializers.CharField(
        source="subscription.plan.name",
        read_only=True
    )

    employer = serializers.CharField(
        source="subscription.employer.company_name",
        read_only=True
    )

    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "plan",
            "employer",
            "amount",
            "currency",
            "gateway",
            "status",
            "transaction_id",
            "gateway_order_id",
            "gateway_payment_id",
            "verified",
            "captured",
            "created_at",
            "updated_at",
        ]