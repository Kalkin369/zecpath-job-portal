from core.views.base_viewset import BaseViewSet
from rest_framework.permissions import IsAuthenticated

from core.models.ai_answer import (
    AIAnswer
)

from core.serializers.ai_answer_serializer import (
    AIAnswerSerializer
)

class AIAnswerViewSet(BaseViewSet):

    queryset = AIAnswer.objects.all()

    serializer_class = (AIAnswerSerializer)

    permission_classes = [IsAuthenticated]