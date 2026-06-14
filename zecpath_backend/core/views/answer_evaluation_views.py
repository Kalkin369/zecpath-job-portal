from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models.ai_answer import AIAnswer
from core.models.answer_evaluation import AnswerEvaluation

from core.services.answer_evaluation_service import (AnswerEvaluationService)

from core.serializers.answer_evaluation_serializer import (AnswerEvaluationSerializer)


class EvaluateAnswerAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        answer_id = request.data.get('answer_id')

        if not answer_id:

            return Response({"error":"answer_id is required"},status=status.HTTP_400_BAD_REQUEST)

        try:

            answer = AIAnswer.objects.get(id=answer_id)

        except AIAnswer.DoesNotExist:

            return Response({"error":"Answer not found"},status=status.HTTP_404_NOT_FOUND)

        keywords = (answer.question.template.expected_keywords)

        keyword_score = (AnswerEvaluationService().calculate_keyword_score(answer.answer_text,keywords))

        total_score = (AnswerEvaluationService().calculate_total_score(keyword_score))

        evaluation, created = (AnswerEvaluation.objects.get_or_create(answer=answer,defaults={
                    
                    "keyword_score":keyword_score,

                    "relevance_score":keyword_score,

                    "completeness_score":keyword_score,

                    "total_score":total_score
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

        return Response(serializer.data,status=status.HTTP_200_OK)


class AnswerEvaluationDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,evaluation_id):

        try:

            evaluation = (AnswerEvaluation.objects.get(id=evaluation_id))

        except AnswerEvaluation.DoesNotExist:

            return Response({"error":"Evaluation not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = (AnswerEvaluationSerializer(evaluation))

        return Response(serializer.data)