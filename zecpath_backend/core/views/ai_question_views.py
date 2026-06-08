from core.views.base_viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated

from core.models.ai_question import (
    AIQuestion
)

from core.serializers.ai_question_serializer import (
    AIQuestionSerializer
)

class AIQuestionViewSet(BaseViewSet):

    queryset = AIQuestion.objects.all()

    serializer_class = (AIQuestionSerializer )

    permission_classes = [IsAuthenticated]