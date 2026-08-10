from core.views.base_viewset import BaseViewSet
from core.permissions import IsAdmin

from core.models.ai_question import (AIQuestion)

from core.throttles import InterviewThrottle

from core.serializers.ai_question_serializer import (AIQuestionSerializer)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

@extend_schema(
    tags=["AI Questions"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List AI Questions",
        description="Retrieve all AI interview questions.",
        responses={
            200: AIQuestionSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve AI Question",
        description="Retrieve an AI interview question by ID.",
        responses={
            200: AIQuestionSerializer,
            404: OpenApiResponse(description="Question not found."),
        },
    ),

    create=extend_schema(
        summary="Create AI Question",
        description="Create a new AI interview question.",
        request=AIQuestionSerializer,
        responses={
            201: AIQuestionSerializer,
            400: OpenApiResponse(description="Validation error."),
        },
    ),

    update=extend_schema(
        summary="Update AI Question",
        description="Update an AI interview question.",
        request=AIQuestionSerializer,
        responses={
            200: AIQuestionSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially Update AI Question",
        description="Update selected fields of an AI interview question.",
        request=AIQuestionSerializer,
        responses={
            200: AIQuestionSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete AI Question",
        description="Delete an AI interview question.",
        responses={
            204: OpenApiResponse(description="Question deleted."),
        },
    ),
)

class AIQuestionViewSet(BaseViewSet):

    queryset = AIQuestion.objects.all()

    serializer_class = AIQuestionSerializer 

    permission_classes = [IsAdmin]

    throttle_classes = [InterviewThrottle]