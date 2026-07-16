from core.models import SubscriptionPlan

from core.permissions import IsAdmin

from core.serializers.subscription_plan_serializer import (
    SubscriptionPlanSerializer
)

from core.views.base_viewset import BaseViewSet


class SubscriptionPlanViewSet(BaseViewSet):

    queryset = (SubscriptionPlan.objects.all())

    serializer_class = (SubscriptionPlanSerializer)

    permission_classes = [IsAdmin]