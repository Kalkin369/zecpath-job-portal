from core.models import PaymentTransaction

from core.permissions import IsAdmin,IsEmployer

from core.serializers.payment_transaction_serializer import (
    PaymentTransactionSerializer
)

from core.views.base_viewset import BaseViewSet

from rest_framework.decorators import action
from rest_framework.response import Response


class PaymentTransactionViewSet(BaseViewSet):

    queryset = (
        PaymentTransaction.objects.select_related(
            "subscription"
        )
    )

    serializer_class = (PaymentTransactionSerializer)

    permission_classes = [IsAdmin]

    def get_permissions(self):

        if self.action == "my_transactions":
            permission_classes = [IsEmployer]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]
    

    

    @action(detail=False, methods=["get"])
    def my_transactions(self, request):

        transactions = (
            PaymentTransaction.objects
            .select_related(
                "subscription",
                "subscription__employer"
            )
            .filter(
                subscription__employer=request.user.employer
            )
            .order_by("-created_at")
        )

        serializer = self.get_serializer(
            transactions,
            many=True
        )

        return Response(serializer.data)