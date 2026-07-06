from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsEmployerOrAdmin

from core.services.recruiter_analytics_service import (RecruiterAnalyticsService)

from django.core.cache import cache

from core.services.logging_service import LoggingService

class RecruiterAnalyticsAPIView(APIView):

    permission_classes = [IsEmployerOrAdmin]

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