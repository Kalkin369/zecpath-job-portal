from django.core.cache import cache
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdmin
from core.serializers.daily_revenue_serializer import DailyRevenueSerializer
from core.serializers.finance_dashboard_serializer import \
    FinanceDashboardSerializer
from core.serializers.monthly_revenue_serializer import \
    MonthlyRevenueSerializer
from core.serializers.payment_failure_serializer import \
    PaymentFailureSerializer
from core.serializers.plan_revenue_serializer import PlanRevenueSerializer
from core.services.finance_service import FinanceService
from core.utils.error_handler import handle_exception


@extend_schema(
    tags=["Finance Analytics"],
    summary="Finance Dashboard",
    description="Retrieve overall financial dashboard metrics.",
    responses={
        200: FinanceDashboardSerializer,
        500: OpenApiResponse(description="Unable to load finance dashboard"),
    },
)
class FinanceDashboardAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            cache_key = "finance_dashboard"

            data = cache.get(cache_key)

            if data is None:

                data = FinanceService().get_dashboard()

                cache.set(cache_key, data, timeout=300)

            serializer = FinanceDashboardSerializer(instance=data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return handle_exception(
                "FinanceDashboardAPIView", e, "Unable to load finance dashboard."
            )


@extend_schema(
    tags=["Finance Analytics"],
    summary="Daily Revenue",
    description="Retrieve daily revenue metrics.",
    responses={
        200: DailyRevenueSerializer(many=True),
        500: OpenApiResponse(description="Unable to load daily revenue"),
    },
)
class DailyRevenueAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = FinanceService().get_daily_revenue()

            serializer = DailyRevenueSerializer(instance=data, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return handle_exception(
                "DailyRevenueAPIView", e, "Unable to load daily revenue."
            )


@extend_schema(
    tags=["Finance Analytics"],
    summary="Monthly Revenue",
    description="Retrieve monthly revenue metrics.",
    responses={
        200: MonthlyRevenueSerializer(many=True),
        500: OpenApiResponse(description="Unable to load monthly revenue"),
    },
)
class MonthlyRevenueAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = FinanceService().get_monthly_revenue()

            serializer = MonthlyRevenueSerializer(instance=data, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return handle_exception(
                "MonthlyRevenueAPIView", e, "Unable to load monthly revenue."
            )


@extend_schema(
    tags=["Finance Analytics"],
    summary="Plan Revenue",
    description="Revenue grouped by subscription plans.",
    responses={
        200: PlanRevenueSerializer(many=True),
        500: OpenApiResponse(description="Unable to load plan revenue"),
    },
)
class PlanRevenueAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = FinanceService().get_plan_revenue()

            serializer = PlanRevenueSerializer(instance=data, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return handle_exception(
                "PlanRevenueAPIView", e, "Unable to load plan revenue."
            )


@extend_schema(
    tags=["Finance Analytics"],
    summary="Payment Failures",
    description="Retrieve failed payment analytics.",
    responses={
        200: PaymentFailureSerializer(many=True),
        500: OpenApiResponse(description="Unable to load failed payments"),
    },
)
class PaymentFailureAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        try:

            data = FinanceService().get_payment_failures()

            serializer = PaymentFailureSerializer(instance=data, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return handle_exception(
                "PaymentFailureAPIView", e, "Unable to load failed payments."
            )
