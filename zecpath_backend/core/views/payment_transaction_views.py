from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import PaymentTransaction
from core.permissions import (
    IsAdmin,
    IsEmployer
)
from core.serializers.payment_transaction_serializer import \
    PaymentTransactionSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Payment Transactions"])
@extend_schema_view(
    list=extend_schema(
        summary="Get Payment Transactions",
        description="Retrieve all payment transactions. Admin only.",
        responses={200: PaymentTransactionSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get Payment Transaction Detail",
        description="Retrieve a payment transaction by ID.",
        responses={200: PaymentTransactionSerializer},
    ),
    create=extend_schema(
        summary="Create Payment Transaction",
        description="Create a payment transaction.",
        request=PaymentTransactionSerializer,
        responses={201: PaymentTransactionSerializer},
    ),
    update=extend_schema(
        summary="Update Payment Transaction",
        request=PaymentTransactionSerializer,
        responses={200: PaymentTransactionSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update Payment Transaction",
        request=PaymentTransactionSerializer,
        responses={200: PaymentTransactionSerializer},
    ),
    destroy=extend_schema(
        summary="Delete Payment Transaction",
        responses={204: OpenApiResponse(description="Deleted successfully.")},
    ),
)
class PaymentTransactionViewSet(BaseViewSet):

    queryset = PaymentTransaction.objects.select_related("subscription")

    serializer_class = PaymentTransactionSerializer

    permission_classes = [IsAdmin]

    def get_permissions(self):

        if self.action == "my_transactions":
            permission_classes = [IsEmployer]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="My Transactions",
        description="Retrieve payment transactions for the authenticated employer.",
        responses={
            200: PaymentTransactionSerializer(many=True),
        },
    )
    @action(detail=False, methods=["get"])
    def my_transactions(self, request):

        transactions = (
            PaymentTransaction.objects.select_related(
                "subscription", "subscription__employer"
            )
            .filter(subscription__employer=request.user.employer)
            .order_by("-created_at")
        )

        serializer = self.get_serializer(transactions, many=True)

        return Response(serializer.data)
