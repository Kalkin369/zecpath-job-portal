from core.models import BillingHistory

from core.permissions import IsAdmin

from core.serializers.billing_history_serializer import (BillingHistorySerializer)

from core.views.base_viewset import BaseViewSet


class BillingHistoryViewSet(BaseViewSet):

    queryset = (
        BillingHistory.objects.select_related(
            "employer",
            "payment"
        )
    )

    serializer_class = (BillingHistorySerializer)

    permission_classes = [IsAdmin]