from core.views.base_viewset import BaseViewSet
from core.permissions import IsAdmin

from core.models.ai_question import (AIQuestion)

from core.throttles import InterviewThrottle

from core.serializers.ai_question_serializer import (AIQuestionSerializer)

class AIQuestionViewSet(BaseViewSet):

    queryset = AIQuestion.objects.all()

    serializer_class = AIQuestionSerializer 

    permission_classes = [IsAdmin]

    throttle_classes = [InterviewThrottle]