from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    inline_serializer
)
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsCandidate
from core.services.flow_manager_service import FlowManagerService
from core.services.question_engine_service import QuestionEngineService
from core.throttles import InterviewThrottle


@extend_schema(
    tags=["AI Interview"],
    summary="Next Interview Question",
    description="Return the next interview question for the current interview session.",
    request=inline_serializer(
        name="NextQuestionRequest",
        fields={
            "role": serializers.CharField(),
            "current_index": serializers.IntegerField(required=False),
        },
    ),
    responses={
        200: OpenApiResponse(description="Question returned successfully."),
        400: OpenApiResponse(description="Invalid request."),
    },
)
class NextQuestionAPIView(APIView):

    permission_classes = [IsCandidate]

    throttle_classes = [InterviewThrottle]

    def post(self, request):

        role = request.data.get("role")

        if not role:
            return Response({"error": "role is required"}, status=400)

        try:

            current_index = int(request.data.get("current_index", 0))

        except ValueError:

            return Response({"error": "Invalid current_index"}, status=400)

        questions = QuestionEngineService().get_questions(role)

        question = FlowManagerService().get_next_question(questions, current_index)

        if question is None:

            return Response({"message": "Interview Completed"})

        return Response(question)


@extend_schema(
    tags=["AI Interview"],
    summary="Submit Candidate Answer",
    description="Submit a candidate's answer and retrieve the next follow-up question if applicable.",
    request=inline_serializer(
        name="SubmitAnswerRequest",
        fields={
            "answer": serializers.CharField(),
            "role": serializers.CharField(),
        },
    ),
    responses={
        200: OpenApiResponse(description="Answer processed successfully."),
        400: OpenApiResponse(description="Answer or role is required."),
    },
)
class SubmitAnswerAPIView(APIView):

    permission_classes = [IsCandidate]

    def post(
        self,
        request,
    ):

        answer = request.data.get("answer")

        if not answer:
            return Response({"error": "answer is required"}, status=400)

        role = request.data.get("role")

        if not role:
            return Response({"error": "role is required"}, status=400)

        next_question = FlowManagerService().get_next_question([], 0, answer, role)

        if next_question is None:

            return Response({"message": "No follow-up question"})

        return Response({"next_question": next_question["question"]})
