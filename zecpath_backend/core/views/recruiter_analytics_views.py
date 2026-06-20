from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (IsAuthenticated)

from core.services.recruiter_analytics_service import (RecruiterAnalyticsService)

from core.models.application import Application

from django.core.cache import cache

class RecruiterAnalyticsAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        analytics_data = cache.get(
            'recruiter_analytics'
        )

        if analytics_data:

            return Response(
                analytics_data
            )

        service = (
            RecruiterAnalyticsService()
        )

        analytics_data = {

            "total_applications":
            Application.objects.count(),

            "funnel":
            service.get_funnel_metrics(),

            "conversion":
            service.get_conversion_rates(),

            "job_performance":
            service.get_job_performance(),

            "time_stats":
            service.get_time_based_stats()
        }

        cache.set(
            'recruiter_analytics',
            analytics_data,
            timeout=300
        )

        return Response(
            analytics_data
        )