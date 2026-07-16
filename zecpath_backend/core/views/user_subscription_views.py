from core.models import UserSubscription

from core.permissions import IsAdmin

from core.serializers.user_subscription_serializer import (
    UserSubscriptionSerializer
)

from core.views.base_viewset import BaseViewSet


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