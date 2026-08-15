from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)
from core.models.ai_interview_session import AIInterviewSession
from core.permissions import IsCandidate, IsEmployer
from core.serializers.ai_interview_session_serializer import \
    AIInterviewSessionSerializer
from core.throttles import InterviewThrottle
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["AI Sessions"])
@extend_schema_view(
    list=extend_schema(summary="List Interview Sessions"),
    retrieve=extend_schema(summary="Retrieve Interview Session"),
    create=extend_schema(summary="Create Interview Session"),
    update=extend_schema(summary="Update Interview Session"),
    partial_update=extend_schema(summary="Partially Update Interview Session"),
    destroy=extend_schema(summary="Delete Interview Session"),
)
class AIInterviewSessionViewSet(BaseViewSet):

    queryset = AIInterviewSession.objects.all()

    serializer_class = AIInterviewSessionSerializer

    throttle_classes = [InterviewThrottle]

    def get_permissions(self):

        if self.action == "list":
            permission_classes = [IsEmployer]
        else:
            permission_classes = [IsCandidate]

        return [permission() for permission in permission_classes]

    def get_queryset(self):

        queryset = self.queryset.select_related("ai_call", "ai_call__application")

        if self.action == "list":

            return queryset.filter(
                ai_call__application__job__employer=self.request.user.employer
            )

        return queryset.filter(
            ai_call__application__candidate=self.request.user.candidate
        )
