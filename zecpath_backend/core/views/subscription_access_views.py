from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema
)
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import (
    HasActiveSubscription,
    IsEmployer
)
from core.serializers.subscription_access_serializer import \
    SubscriptionAccessSerializer
from core.services.subscription_service import SubscriptionService


@extend_schema(
    tags=["Subscription Access"],
    summary="Check Subscription Access",
    description="Return the authenticated employer's subscription features and limits.",
    responses={
        200: SubscriptionAccessSerializer,
        403: OpenApiResponse(
            description="Employer does not have an active subscription."
        ),
    },
)
class SubscriptionAccessAPIView(APIView):

    permission_classes = [
        IsEmployer,
        HasActiveSubscription,
    ]

    def get(self, request):

        employer = request.user.employer

        data = SubscriptionService().get_subscription_access(employer)

        serializer = SubscriptionAccessSerializer(instance=data)

        return Response(serializer.data)
