from rest_framework import viewsets
from core.permissions import IsAdmin

from core.models.call_log import CallLog

from core.serializers.call_log_serializer import (CallLogSerializer)

from drf_spectacular.utils import extend_schema,extend_schema_view,OpenApiResponse

@extend_schema(
    tags=["Call Logs"]
)

@extend_schema_view(

    list=extend_schema(
        summary="List Call Logs",
        description="Retrieve AI interview call logs.",
        responses={
            200: CallLogSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Call Log",
        description="Retrieve a call log.",
        responses={
            200: CallLogSerializer,
            404: OpenApiResponse(
                description="Call log not found."
            ),
        },
    ),
)

class CallLogViewSet( viewsets.ReadOnlyModelViewSet):

    queryset = CallLog.objects.all()

    serializer_class = CallLogSerializer

    permission_classes = [IsAdmin]