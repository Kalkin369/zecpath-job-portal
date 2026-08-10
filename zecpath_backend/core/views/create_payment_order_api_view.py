from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsEmployer

from core.serializers.create_payment_order_serializer import (
    CreatePaymentOrderSerializer
)

from core.services.payment_gateway_service import (
    PaymentGatewayService
)

from drf_spectacular.utils import extend_schema,OpenApiResponse

@extend_schema(
    tags=["Payment Gateway"],
    summary="Create Payment Order",
    description="Create a Razorpay order for a subscription purchase.",
    request=CreatePaymentOrderSerializer,
    responses={
        201: OpenApiResponse(
            description="Payment order created successfully."
        ),
        400: OpenApiResponse(
            description="Invalid subscription."
        ),
        403: OpenApiResponse(
            description="Employer authentication required."
        ),
    },
)


class CreatePaymentOrderAPIView(APIView):

    permission_classes = [
        IsEmployer
    ]

    def post(
        self,
        request
    ):

        serializer = CreatePaymentOrderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = PaymentGatewayService().create_payment_order(
            employer=request.user.employer,
            subscription_id=serializer.validated_data[
                "subscription_id"
            ]
        )

        order = result["order"]

        return Response(
            {
                "message": "Payment order created successfully.",
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "status": order["status"]
            },
            status=status.HTTP_201_CREATED
        )