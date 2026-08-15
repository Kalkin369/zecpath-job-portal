from django.core.cache import cache
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import CanUseAnalytics, IsEmployer
from core.serializers.candidate_prediction_serializer import \
    CandidatePredictionSerializer
from core.serializers.candidate_ranking_serializer import \
    CandidateRankingSerializer
from core.serializers.hiring_efficiency_serializer import \
    HiringEfficiencySerializer
from core.serializers.premium_dashboard_serializer import \
    PremiumDashboardSerializer
from core.services.premium_recruiter_service import PremiumRecruiterService
from core.throttles import PremiumRecruiterThrottle
from core.utils.error_handler import handle_exception


@extend_schema(
    tags=["Premium Analytics"],
    summary="Candidate Ranking",
    description=(
        "Retrieve AI-ranked candidates based on ATS score, interview "
        "performance, and hiring metrics."
    ),
    responses={
        200: CandidateRankingSerializer(many=True),
        403: OpenApiResponse(description="Premium analytics subscription required."),
        500: OpenApiResponse(description="Unable to generate candidate ranking."),
    },
)
class CandidateRankingAPIView(APIView):

    permission_classes = [IsEmployer, CanUseAnalytics]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            data = PremiumRecruiterService().get_candidate_ranking(
                request.user.employer
            )

            serializer = CandidateRankingSerializer(instance=data, many=True)

            return Response(serializer.data)

        except Exception as e:

            return handle_exception(
                "CandidateRankingAPIView", e, "Unable to generate candidate ranking."
            )


@extend_schema(
    tags=["Premium Analytics"],
    summary="Hiring Efficiency Report",
    description=(
        "Retrieve hiring efficiency statistics for the authenticated employer."
    ),
    responses={
        200: HiringEfficiencySerializer,
        403: OpenApiResponse(description="Premium analytics subscription required."),
        500: OpenApiResponse(
            description="Unable to generate hiring efficiency report."
        ),
    },
)
class HiringEfficiencyAPIView(APIView):

    permission_classes = [IsEmployer, CanUseAnalytics]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            data = PremiumRecruiterService().get_hiring_efficiency(
                request.user.employer
            )

            serializer = HiringEfficiencySerializer(instance=data)

            return Response(serializer.data)

        except Exception as e:

            return handle_exception(
                "HiringEfficiencyAPIView",
                e,
                "Unable to generate hiring efficiency report.",
            )


@extend_schema(
    tags=["Premium Analytics"],
    summary="Candidate Success Prediction",
    description=(
        "Retrieve AI-generated predictions indicating the likelihood of "
        "candidate success."
    ),
    responses={
        200: CandidatePredictionSerializer(many=True),
        403: OpenApiResponse(description="Premium analytics subscription required."),
        500: OpenApiResponse(description="Unable to generate prediction report."),
    },
)
class CandidatePredictionAPIView(APIView):

    permission_classes = [IsEmployer, CanUseAnalytics]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            data = PremiumRecruiterService().get_candidate_predictions(
                request.user.employer
            )

            serializer = CandidatePredictionSerializer(instance=data, many=True)

            return Response(serializer.data)

        except Exception as e:

            return handle_exception(
                "CandidatePredictionAPIView", e, "Unable to generate prediction report."
            )


@extend_schema(
    tags=["Premium Analytics"],
    summary="Premium Recruiter Dashboard",
    description=(
        "Retrieve the premium recruiter dashboard including hiring KPIs, "
        "AI insights, candidate rankings, and predictive analytics."
    ),
    responses={
        200: PremiumDashboardSerializer,
        403: OpenApiResponse(description="Premium analytics subscription required."),
        500: OpenApiResponse(description="Unable to load premium dashboard."),
    },
)
class PremiumDashboardAPIView(APIView):

    permission_classes = [IsEmployer, CanUseAnalytics]

    throttle_classes = [PremiumRecruiterThrottle]

    def get(self, request):

        try:

            cache_key = f"premium_dashboard_{request.user.id}"

            dashboard_data = cache.get(cache_key)

            if dashboard_data is None:

                dashboard_data = PremiumRecruiterService().get_dashboard(
                    request.user.employer
                )

                cache.set(cache_key, dashboard_data, timeout=300)

            serializer = PremiumDashboardSerializer(instance=dashboard_data)

            return Response(serializer.data)

        except Exception as e:

            return handle_exception(
                "PremiumDashboardAPIView", e, "Unable to load premium dashboard."
            )
