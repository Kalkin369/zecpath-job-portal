from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models.call_log import CallLog

from core.serializers.call_log_serializer import (
    CallLogSerializer
)

class CallLogViewSet( viewsets.ReadOnlyModelViewSet):

    queryset = CallLog.objects.all()

    serializer_class = (CallLogSerializer)

    permission_classes = [IsAuthenticated]