from rest_framework import viewsets
from core.permissions import IsAdmin

from core.models.notification_log import NotificationLog
from core.serializers.notification_log_serializer import ( NotificationLogSerializer )


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset =NotificationLog.objects.all().order_by('-created_at')
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAdmin]