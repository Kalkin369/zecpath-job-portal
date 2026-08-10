from core.models import BillingHistory

from core.permissions import IsAdmin

from core.serializers.billing_history_serializer import (BillingHistorySerializer)

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema,extend_schema_view,OpenApiResponse

@extend_schema(tags=["Billing History"])
@extend_schema_view(
    list=extend_schema(
        summary="Get Billing History",
        description="Retrieve all billing history records.",
        responses={
            200: BillingHistorySerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Get Billing History Detail",
        description="Retrieve a billing history record by ID.",
        responses={
            200: BillingHistorySerializer,
            404: OpenApiResponse(
                description="Billing history not found."
            ),
        },
    ),
)


class BillingHistoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    queryset = (
        BillingHistory.objects.select_related(
            "employer",
            "payment"
        )
    )

    serializer_class = (BillingHistorySerializer)

    permission_classes = [IsAdmin]