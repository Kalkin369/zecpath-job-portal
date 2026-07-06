from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsCandidate

from core.services.question_engine_service import (QuestionEngineService)

from core.services.flow_manager_service import (FlowManagerService)


class NextQuestionAPIView(APIView):

    permission_classes = [IsCandidate]

    def post(self,request):

        role = request.data.get('role')

        if not role:
            return Response({"error":"role is required"},status=400)
        
        try:    

           current_index = int(request.data.get('current_index',0))

        except ValueError:

           return Response({"error":"Invalid current_index"},status=400)    

        questions = (QuestionEngineService().get_questions(role))

        question = (FlowManagerService().get_next_question(questions,current_index))

        if question is None:

            return Response({"message":"Interview Completed"})

        return Response(question)
    
class SubmitAnswerAPIView(APIView):

    permission_classes = [IsCandidate]

    def post(self,request,):

        answer = request.data.get('answer')

        if not answer:
            return Response({"error":"answer is required"},status=400)
        
        role = request.data.get('role')

        if not role:
            return Response({"error":"role is required"},status=400)
        

        next_question = (FlowManagerService().get_next_question([],0,answer,role))

        if next_question is None:

            return Response({"message":"No follow-up question"})

        return Response({"next_question":next_question["question"]})    