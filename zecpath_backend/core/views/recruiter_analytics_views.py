from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsEmployerOrAdmin,CanUseAnalytics

from core.services.recruiter_analytics_service import (RecruiterAnalyticsService)

from django.core.cache import cache

from core.services.logging_service import LoggingService

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)

@extend_schema(
    tags=["Recruiter Analytics"],
    summary="Recruiter Analytics Dashboard",
    description=(
        "Retrieve recruiter analytics including application statistics, "
        "conversion funnel, hiring performance, and time-based metrics."
    ),
    responses={
        200: OpenApiResponse(
            description="Analytics retrieved successfully."
        ),
        403: OpenApiResponse(
            description="Employer with analytics subscription required."
        ),
        500: OpenApiResponse(
            description="Unable to load analytics."
        ),
    },
    examples=[
        OpenApiExample(
            "Analytics Response",
            value={
                "total_applications": 125,
                "funnel": {},
                "conversion": {},
                "job_performance": {},
                "time_stats": {}
            },
            response_only=True,
        )
    ],
)

class RecruiterAnalyticsAPIView(APIView):

    permission_classes = [IsEmployerOrAdmin,CanUseAnalytics]

    def get(self,request):
      
      try:    

        cache_key = (f"analytics_{request.user.id}")

        analytics_data = cache.get(cache_key)

        if analytics_data:

            return Response(
                analytics_data
            )

        service = RecruiterAnalyticsService()

        applications = (service.get_applications(request.user))

        analytics_data = {

            "total_applications":
            applications.count(),

            "funnel":
            service.get_funnel_metrics(
                request.user
            ),

            "conversion":
            service.get_conversion_rates(
                request.user
            ),

            "job_performance":
            service.get_job_performance(
                request.user
            ),

            "time_stats":
            service.get_time_based_stats(
                request.user
            )
        }

        cache.set(
            cache_key,
            analytics_data,
            timeout=300
        )

        return Response(
            analytics_data
        )
      except Exception as e:

        LoggingService().create_error_log("RecruiterAnalyticsAPIView",str(e))

        return Response({"success":False,"message":"Unable to load analytics"},status=500)