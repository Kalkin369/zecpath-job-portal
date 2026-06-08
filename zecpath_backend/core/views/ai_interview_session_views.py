from core.views.base_viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated

from core.models.ai_interview_session import (
    AIInterviewSession
)

from core.serializers.ai_interview_session_serializer import (
    AIInterviewSessionSerializer
)

class AIInterviewSessionViewSet(BaseViewSet):

    queryset = AIInterviewSession.objects.all()

    serializer_class = (AIInterviewSessionSerializer)

    permission_classes = [IsAuthenticated ]