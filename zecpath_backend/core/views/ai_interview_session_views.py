from core.views.base_viewset import BaseViewSet
from core.permissions import IsCandidate

from core.models.ai_interview_session import (AIInterviewSession)

from core.serializers.ai_interview_session_serializer import (AIInterviewSessionSerializer)


class AIInterviewSessionViewSet(BaseViewSet):

    serializer_class = (AIInterviewSessionSerializer)

    permission_classes = [IsCandidate]

    def get_queryset(self,):
        return (AIInterviewSession.objects.select_related("ai_call","ai_call_application").filter
        (ai_call__application__candidate=self.request.user.candidate))