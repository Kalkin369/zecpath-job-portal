from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from core.permissions import IsAdmin,IsEmployer
from rest_framework import status

from core.models.ai_answer import AIAnswer
from core.models.answer_evaluation import AnswerEvaluation

from core.services.answer_evaluation_service import (AnswerEvaluationService)

from core.serializers.answer_evaluation_serializer import (AnswerEvaluationSerializer)
from core.services.logging_service import (LoggingService)


class EvaluateAnswerAPIView(APIView):

    permission_classes = [IsAdmin]

    def post(self,request):

        answer_id = (request.data.get('answer_id'))

        if not answer_id:

            return Response({"error":"answer_id is required"},status=status.HTTP_400_BAD_REQUEST)

        try:

            answer = get_object_or_404(AIAnswer,id=answer_id)

            keywords = (answer.question.template.expected_keywords
                if answer.question.template
                else []
            )

            keyword_score = (AnswerEvaluationService().calculate_keyword_score(answer.answer_text,keywords))

            total_score = (AnswerEvaluationService().calculate_total_score(keyword_score))

            evaluation, created = (
                AnswerEvaluation.objects
                .get_or_create(
                    answer=answer,
                    defaults={
                        "keyword_score":
                        keyword_score,

                        "relevance_score":
                        keyword_score,

                        "completeness_score":
                        keyword_score,

                        "total_score":
                        total_score
                    }
                )
            )

            if not created:

                evaluation.keyword_score = (keyword_score)

                evaluation.relevance_score = (keyword_score)

                evaluation.completeness_score = (keyword_score)

                evaluation.total_score = (total_score)

                evaluation.save()

            serializer = (AnswerEvaluationSerializer(evaluation))

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Http404:

            LoggingService().create_error_log(
                "EvaluateAnswerAPIView",
                f"Answer {answer_id} not found"
            )

            return Response(
                {
                    "error":
                    "Answer not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:

            LoggingService().create_error_log(
                "EvaluateAnswerAPIView",
                str(e)
            )

            return Response(
                {
                    "error":
                    "Evaluation failed"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AnswerEvaluationDetailAPIView(APIView):

    permission_classes = [IsEmployer]

    def get(self,request,evaluation_id):

        try:

            evaluation = (AnswerEvaluation.objects.filter(answer__question__session__ai_call__application__job__employer=request.user.employer)
                          .get(id=evaluation_id))

        except AnswerEvaluation.DoesNotExist:

            return Response({"error":"Evaluation not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = (AnswerEvaluationSerializer(evaluation))

        return Response(serializer.data)