from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)
from rest_framework import viewsets

from core.models.ai_call import AICall
from core.permissions import IsEmployerOrAdmin
from core.serializers.ai_call_serializer import AICallSerializer
from core.throttles import InterviewThrottle


@extend_schema(tags=["AI Calls"])
@extend_schema_view(
    list=extend_schema(summary="List AI Calls"),
    retrieve=extend_schema(summary="Retrieve AI Call"),
    create=extend_schema(summary="Create AI Call"),
    update=extend_schema(summary="Update AI Call"),
    partial_update=extend_schema(summary="Partially Update AI Call"),
    destroy=extend_schema(summary="Delete AI Call"),
)
class AICallViewSet(viewsets.ModelViewSet):

    serializer_class = AICallSerializer

    permission_classes = [IsEmployerOrAdmin]

    throttle_classes = [InterviewThrottle]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return AICall.objects.none()

        if self.request.user.role == "admin":
            return AICall.objects.all().order_by("-created_at")

        return AICall.objects.filter(
            application__job__employer=self.request.user.employer
        ).order_by("-created_at")
