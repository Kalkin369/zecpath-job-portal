from core.views.base_viewset import BaseViewSet
from core.permissions import IsCandidate
from core.models.ai_answer import AIAnswer
from core.serializers.ai_answer_serializer import AIAnswerSerializer


class AIAnswerViewSet(BaseViewSet):

    queryset = AIAnswer.objects.all()

    serializer_class = AIAnswerSerializer

    permission_classes = [IsCandidate]

    def get_queryset(self):

        return (
            self.queryset
            .select_related(
                "question",
                "question__session",
                "question__session__ai_call",
                "question__session__ai_call__application"
            )
            .filter(
                question__session__ai_call__application__candidate=self.request.user.candidate
            )
        )