from core.views.base_viewset import BaseViewSet
from core.permissions import IsCandidate
from core.throttles import InterviewThrottle
from core.models.ai_answer import AIAnswer
from core.serializers.ai_answer_serializer import AIAnswerSerializer

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

@extend_schema(
    tags=["AI Answers"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List AI Answers",
        description="Retrieve interview answers belonging to the authenticated candidate.",
        responses={
            200: AIAnswerSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve AI Answer",
        description="Retrieve a candidate's interview answer.",
        responses={
            200: AIAnswerSerializer,
            404: OpenApiResponse(description="Answer not found."),
        },
    ),

    create=extend_schema(
        summary="Create AI Answer",
        description="Submit an AI interview answer.",
        request=AIAnswerSerializer,
        responses={
            201: AIAnswerSerializer,
            400: OpenApiResponse(description="Validation error."),
        },
    ),

    update=extend_schema(
        summary="Update AI Answer",
        description="Update an AI interview answer.",
        request=AIAnswerSerializer,
        responses={
            200: AIAnswerSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially Update AI Answer",
        description="Update selected fields of an AI interview answer.",
        request=AIAnswerSerializer,
        responses={
            200: AIAnswerSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete AI Answer",
        description="Delete an AI interview answer.",
        responses={
            204: OpenApiResponse(description="Answer deleted."),
        },
    ),
)


class AIAnswerViewSet(BaseViewSet):

    queryset = AIAnswer.objects.all()

    serializer_class = AIAnswerSerializer

    permission_classes = [IsCandidate]

    throttle_classes = [InterviewThrottle]

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