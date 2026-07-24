from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import (IsEmployer,CanUseAnalytics)

from core.services.premium_recruiter_service import (PremiumRecruiterService)

from core.services.logging_service import (LoggingService)

from core.throttles import PremiumRecruiterThrottle

from django.core.cache import cache


class CandidateRankingAPIView(APIView):

    permission_classes = [
        IsEmployer,
        CanUseAnalytics
    ]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            data = (
                PremiumRecruiterService()
                .get_candidate_ranking(
                    request.user.employer
                )
            )

            return Response(
                data
            )

        except Exception as e:

            LoggingService().create_error_log(
                "CandidateRankingAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to generate candidate ranking."
                },
                status=500
            )


class HiringEfficiencyAPIView(APIView):

    permission_classes = [
        IsEmployer,
        CanUseAnalytics
    ]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            data = (
                PremiumRecruiterService()
                .get_hiring_efficiency(
                    request.user.employer
                )
            )

            return Response(
                data
            )

        except Exception as e:

            LoggingService().create_error_log(
                "HiringEfficiencyAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to generate hiring efficiency report."
                },
                status=500
            )


class CandidatePredictionAPIView(APIView):

    permission_classes = [
        IsEmployer,
        CanUseAnalytics
    ]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            data = (
                PremiumRecruiterService()
                .get_candidate_predictions(
                    request.user.employer
                )
            )

            return Response(
                data
            )

        except Exception as e:

            LoggingService().create_error_log(
                "CandidatePredictionAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to generate prediction report."
                },
                status=500
            )



class PremiumDashboardAPIView(APIView):

    permission_classes = [
        IsEmployer,
        CanUseAnalytics
    ]

    throttle_classes = [
        PremiumRecruiterThrottle
    ]

    def get(self, request):

        try:

            cache_key = (
                f"premium_dashboard_{request.user.id}"
            )

            dashboard_data = cache.get(
                cache_key
            )

            if dashboard_data:

                return Response(
                    dashboard_data
                )

            dashboard_data = (
                PremiumRecruiterService()
                .get_dashboard(
                    request.user.employer
                )
            )

            cache.set(
                cache_key,
                dashboard_data,
                timeout=300
            )

            return Response(
                dashboard_data
            )

        except Exception as e:

            LoggingService().create_error_log(
                "PremiumDashboardAPIView",
                str(e)
            )

            return Response(
                {
                    "success": False,
                    "message": "Unable to load premium dashboard."
                },
                status=500
            )