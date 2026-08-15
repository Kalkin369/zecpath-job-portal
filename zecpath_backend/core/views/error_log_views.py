from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.models import ErrorLog
from core.permissions import IsAdmin
from core.serializers.error_log_serializer import ErrorLogSerializer


@extend_schema(tags=["Error Logs"])
@extend_schema_view(
    list=extend_schema(
        summary="List Error Logs",
        description="Retrieve application error logs.",
        responses={
            200: ErrorLogSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Error Log",
        description="Retrieve an error log by ID.",
        responses={
            200: ErrorLogSerializer,
            404: OpenApiResponse(description="Error log not found."),
        },
    ),
)
class ErrorLogViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    queryset = ErrorLog.objects.all().order_by("-created_at")

    serializer_class = ErrorLogSerializer

    permission_classes = [IsAdmin]
