from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsEmployer
from core.serializers.payment_history_serializer import \
    PaymentHistorySerializer
from core.services.payment_gateway_service import PaymentGatewayService


@extend_schema(
    tags=["Payment Gateway"],
    summary="Get Payment History",
    description="Retrieve payment history for the authenticated employer.",
    responses={
        200: PaymentHistorySerializer(many=True),
        403: OpenApiResponse(description="Employer authentication required."),
    },
)
class PaymentHistoryAPIView(APIView):

    permission_classes = [IsEmployer]

    def get(self, request):

        service = PaymentGatewayService()

        payments = service.get_payment_history(employer=request.user.employer)

        serializer = PaymentHistorySerializer(payments, many=True)

        return Response(
            {"success": True, "count": len(serializer.data), "data": serializer.data},
            status=status.HTTP_200_OK,
        )
