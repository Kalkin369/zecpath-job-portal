from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from core.permissions import IsEmployer

from core.serializers.verify_payment_serializer import (
    VerifyPaymentSerializer
)

from core.services.payment_gateway_service import (
    PaymentGatewayService
)


class VerifyPaymentAPIView(APIView):

    permission_classes = [
        IsEmployer
    ]

    def post(
        self,
        request
    ):

        serializer = VerifyPaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = (
            PaymentGatewayService().verify_payment(
                **serializer.validated_data
            )
        )

        if not result["success"]:

            return Response(
                result,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            result,
            status=status.HTTP_200_OK
        )