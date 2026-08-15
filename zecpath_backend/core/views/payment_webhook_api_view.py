from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers.payment_webhook_serializer import \
    PaymentWebhookSerializer
from core.services.payment_gateway_service import PaymentGatewayService


@extend_schema(
    tags=["Payment Gateway"],
    summary="Payment Webhook",
    description="Webhook endpoint called by Razorpay for payment events.",
    request=PaymentWebhookSerializer,
    responses={
        200: OpenApiResponse(description="Webhook processed successfully."),
        400: OpenApiResponse(description="Invalid webhook signature."),
    },
)
class PaymentWebhookAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = PaymentWebhookSerializer(
            data={"signature": request.headers.get("X-Razorpay-Signature")}
        )

        serializer.is_valid(raise_exception=True)

        result = PaymentGatewayService().process_webhook(
            payload=request.body,  # Raw payload
            signature=serializer.validated_data["signature"],
        )

        return Response(result, status=status.HTTP_200_OK)
