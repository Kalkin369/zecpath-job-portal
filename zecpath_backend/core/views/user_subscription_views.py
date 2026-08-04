from core.models import UserSubscription

from core.permissions import IsAdmin,IsEmployer

from core.serializers.user_subscription_serializer import (
    UserSubscriptionSerializer
)

from core.views.base_viewset import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class UserSubscriptionViewSet(BaseViewSet):

    queryset = (
        UserSubscription.objects.select_related(
            "employer",
            "plan"
        )
    )

    serializer_class = (
        UserSubscriptionSerializer
    )

    permission_classes = [
        IsAdmin
    ]

    def get_permissions(self):

        if self.action == "my_subscription":
            permission_classes = [IsEmployer]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]

    

    @action(detail=False, methods=["get"])
    def my_subscription(self, request):

        subscription = (
            UserSubscription.objects
            .select_related("plan", "employer")
            .filter(
                employer=request.user.employer,
                is_active=True
            )
            .first()
        )

        if not subscription:
            return Response(
                {"message": "No active subscription found."},
                status=404
            )

        serializer = self.get_serializer(subscription)

        return Response(serializer.data)