from core.models import PaymentTransaction

from core.permissions import IsAdmin

from core.serializers.payment_transaction_serializer import (
    PaymentTransactionSerializer
)

from core.views.base_viewset import BaseViewSet


class PaymentTransactionViewSet(BaseViewSet):

    queryset = (
        PaymentTransaction.objects.select_related(
            "subscription"
        )
    )

    serializer_class = (PaymentTransactionSerializer)

    permission_classes = [IsAdmin]