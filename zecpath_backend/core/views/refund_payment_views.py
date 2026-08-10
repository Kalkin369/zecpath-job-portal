from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsEmployer

from core.serializers.refund_payment_serializer import RefundPaymentSerializer
from core.services.payment_gateway_service import PaymentGatewayService
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)


@extend_schema(
    tags=["Payment Gateway"],
    summary="Refund Payment",
    description="Initiate a refund for a successful payment.",

    request=RefundPaymentSerializer,

    responses={
        200: OpenApiResponse(
            description="Refund initiated successfully."
        ),
        400: OpenApiResponse(
            description="Invalid payment ID or refund request."
        ),
        403: OpenApiResponse(
            description="Employer authentication required."
        ),
    },

    examples=[
        OpenApiExample(
            name="Successful Refund",
            value={
                "success": True,
                "message": "Refund initiated successfully.",
                "data": {
                    "refund_id": "rfnd_QWERTY123456",
                    "status": "pending"
                }
            },
            response_only=True,
        )
    ],
)

class RefundPaymentAPIView(APIView):

    permission_classes = [IsEmployer]

    def post(
        self,
        request
    ):

        serializer = RefundPaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        refund = PaymentGatewayService().process_refund(
            employer=request.user.employer,
            payment_id=serializer.validated_data["payment_id"],
            amount=serializer.validated_data["amount"]
        )

        return Response(
            {
                "success": True,
                "message": "Refund initiated successfully.",
                "data": refund
            },
            status=status.HTTP_200_OK
        )