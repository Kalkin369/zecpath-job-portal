from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.permissions import IsEmployer
from core.serializers.verify_payment_serializer import VerifyPaymentSerializer
from core.services.payment_gateway_service import PaymentGatewayService


@extend_schema(
    tags=["Payment Gateway"],
    summary="Verify Payment",
    description="Verify Razorpay payment signature after checkout.",
    request=VerifyPaymentSerializer,
    responses={
        200: OpenApiResponse(description="Payment verified successfully."),
        400: OpenApiResponse(description="Payment verification failed."),
        403: OpenApiResponse(description="Employer authentication required."),
    },
)
class VerifyPaymentAPIView(APIView):

    permission_classes = [IsEmployer]

    def post(self, request):

        serializer = VerifyPaymentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        result = PaymentGatewayService().verify_payment(**serializer.validated_data)

        if not result["success"]:

            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
