from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsEmployer,HasActiveSubscription

from core.services.subscription_service import (
    SubscriptionService
)


class SubscriptionAccessAPIView(APIView):

    permission_classes = [
        IsEmployer,
        HasActiveSubscription,
    ]

    def get(self, request):

        employer = request.user.employer

        data = SubscriptionService().get_subscription_access(employer)

        return Response(data)