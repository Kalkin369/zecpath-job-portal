from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import (IsEmployer,CanUseAnalytics)

from core.services.premium_recruiter_service import (PremiumRecruiterService)

from core.services.logging_service import (LoggingService)

from core.throttles import PremiumRecruiterThrottle

from django.core.cache import cache

from core.serializers.candidate_ranking_serializer import (CandidateRankingSerializer)
from core.serializers.hiring_efficiency_serializer import (HiringEfficiencySerializer)
from core.serializers.candidate_prediction_serializer import (CandidatePredictionSerializer)
from core.serializers.premium_dashboard_serializer import (PremiumDashboardSerializer)

from rest_framework import status


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

            serializer =CandidateRankingSerializer(instance=data, many=True)

            return Response(
                serializer.data
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

            serializer = HiringEfficiencySerializer(instance=data)

            return Response(
                serializer.data
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

            serializer = CandidatePredictionSerializer(instance=data, many=True)

            return Response(
                serializer.data
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

            if  dashboard_data is None:

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

            serializer = PremiumDashboardSerializer(instance=dashboard_data)

            return Response(
                serializer.data
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )