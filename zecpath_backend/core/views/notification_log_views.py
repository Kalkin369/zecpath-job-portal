from drf_spectacular.utils import (
    OpenApiResponse, 
    extend_schema,
    extend_schema_view
)
from rest_framework import viewsets

from core.models.notification_log import NotificationLog
from core.permissions import IsAdmin
from core.serializers.notification_log_serializer import \
    NotificationLogSerializer


@extend_schema(tags=["Notification Logs"])
@extend_schema_view(
    list=extend_schema(
        summary="List Notification Logs",
        description="Retrieve all notification delivery logs.",
        responses={
            200: NotificationLogSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Notification Log",
        description="Retrieve a notification log by ID.",
        responses={
            200: NotificationLogSerializer,
            404: OpenApiResponse(description="Notification log not found."),
        },
    ),
)
class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = NotificationLog.objects.all().order_by("-created_at")

    serializer_class = NotificationLogSerializer

    permission_classes = [IsAdmin]
