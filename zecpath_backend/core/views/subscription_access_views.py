from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsEmployer,HasActiveSubscription

from core.services.subscription_service import (SubscriptionService)

from core.serializers.subscription_access_serializer import (SubscriptionAccessSerializer)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

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