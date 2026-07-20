from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsEmployer

from core.serializers.refund_payment_serializer import RefundPaymentSerializer
from core.services.payment_gateway_service import PaymentGatewayService


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