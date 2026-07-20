from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from core.serializers.payment_detail_serializer import PaymentDetailSerializer
from core.services.payment_gateway_service import PaymentGatewayService
from core.permissions import IsEmployer
from core.models.payment_transaction import PaymentTransaction


class PaymentDetailAPIView(APIView):

    permission_classes = [IsEmployer]

    def get(
        self,
        request,
        payment_id
    ):

        service = PaymentGatewayService()

        try:

            payment = service.get_payment_detail(
                employer=request.user.employer,
                payment_id=payment_id
            )

        except PaymentTransaction.DoesNotExist:
            raise Http404("Payment not found.")

        serializer = PaymentDetailSerializer(payment)

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )