from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.models import AuditTrail
from core.permissions import IsAdmin
from core.serializers.audit_trail_serializer import AuditTrailSerializer


@extend_schema(tags=["Audit Logs"])
@extend_schema_view(
    list=extend_schema(
        summary="List Audit Logs",
        description="Retrieve system audit trail records.",
        responses={
            200: AuditTrailSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Audit Log",
        description="Retrieve an audit log by ID.",
        responses={
            200: AuditTrailSerializer,
            404: OpenApiResponse(description="Audit log not found."),
        },
    ),
)
class AuditTrailViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    queryset = AuditTrail.objects.select_related("user").order_by("-created_at")

    serializer_class = AuditTrailSerializer

    permission_classes = [IsAdmin]
