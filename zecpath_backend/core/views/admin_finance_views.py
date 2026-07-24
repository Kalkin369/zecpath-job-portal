from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsAdmin

from core.services.finance_service import (
    FinanceService
)

from core.services.logging_service import (
    LoggingService
)

from core.serializers.finance_dashboard_serializer import (
    FinanceDashboardSerializer
)

from core.serializers.daily_revenue_serializer import (
    DailyRevenueSerializer
)

from core.serializers.monthly_revenue_serializer import (
    MonthlyRevenueSerializer
)

from core.serializers.plan_revenue_serializer import (
    PlanRevenueSerializer
)

from core.serializers.payment_failure_serializer import (
    PaymentFailureSerializer
)

class FinanceDashboardAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            cache_key = "finance_dashboard"

            data = cache.get(cache_key)

            if data is None:

                
                data = (
                    FinanceService()
                    .get_dashboard()
                )

                cache.set(
                    cache_key,
                    data,
                    timeout=300
                )

            serializer = FinanceDashboardSerializer(instance=data)

            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:

            LoggingService().create_error_log(
                "FinanceDashboardAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to load finance dashboard."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DailyRevenueAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = (
                FinanceService()
                .get_daily_revenue()
            )

            serializer = DailyRevenueSerializer(instance=data, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e:

            LoggingService().create_error_log(
                "DailyRevenueAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to load daily revenue."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MonthlyRevenueAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = (
                FinanceService()
                .get_monthly_revenue()
            )

            serializer = MonthlyRevenueSerializer(instance=data, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:

            LoggingService().create_error_log(
                "MonthlyRevenueAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to load monthly revenue."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlanRevenueAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = (
                FinanceService()
                .get_plan_revenue()
            )

            serializer = PlanRevenueSerializer(instance=data, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:

            LoggingService().create_error_log(
                "PlanRevenueAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to load plan revenue."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentFailureAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = FinanceService().get_payment_failures()

            serializer = PaymentFailureSerializer(instance=data, many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:

            LoggingService().create_error_log(
                "PaymentFailureAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to load failed payments."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )