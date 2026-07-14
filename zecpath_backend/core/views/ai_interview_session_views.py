from core.views.base_viewset import BaseViewSet
from core.permissions import IsCandidate, IsEmployer
from core.models.ai_interview_session import AIInterviewSession
from core.serializers.ai_interview_session_serializer import (
    AIInterviewSessionSerializer
)


class AIInterviewSessionViewSet(BaseViewSet):

    queryset = AIInterviewSession.objects.all()

    serializer_class = AIInterviewSessionSerializer

    def get_permissions(self):

        if self.action == "list":
            permission_classes = [IsEmployer]
        else:
            permission_classes = [IsCandidate]

        return [permission() for permission in permission_classes]

    def get_queryset(self):

        queryset = (
            self.queryset
            .select_related(
                "ai_call",
                "ai_call__application"
            )
        )

        if self.action == "list":

            return queryset.filter(
                ai_call__application__job__employer=self.request.user.employer
            )

        return queryset.filter(
            ai_call__application__candidate=self.request.user.candidate
        )