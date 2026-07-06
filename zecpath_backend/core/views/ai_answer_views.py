from core.views.base_viewset import BaseViewSet

from core.permissions import IsCandidate

from core.models.ai_answer import (AIAnswer)

from core.serializers.ai_answer_serializer import (AIAnswerSerializer)

class AIAnswerViewSet(BaseViewSet):

    serializer_class = AIAnswerSerializer

    permission_classes = [IsCandidate]

    def get_queryset(self):

        return AIAnswer.objects.filter(question__session__candidate=self.request.user.candidate)