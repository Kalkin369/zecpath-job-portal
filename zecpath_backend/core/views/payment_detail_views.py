from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from core.serializers.payment_detail_serializer import PaymentDetailSerializer
from core.services.payment_gateway_service import PaymentGatewayService
from core.permissions import IsEmployer
from core.models.payment_transaction import PaymentTransaction
from drf_spectacular.utils import extend_schema,OpenApiResponse

@extend_schema(
    tags=["Payment Gateway"],
    summary="Get Payment Detail",
    description="Retrieve a payment transaction by payment ID.",
    responses={
        200: PaymentDetailSerializer,
        404: OpenApiResponse(
            description="Payment not found."
        ),
        403: OpenApiResponse(
            description="Employer authentication required."
        ),
    },
)


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