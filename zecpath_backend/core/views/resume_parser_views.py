from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsCandidate

from core.services.resume_parser_service import (extract_resume_text)
from core.services.resume_nlp_service import (build_resume_json)
from core.services.logging_service import LoggingService


class ResumeParserAPIView(APIView):

    permission_classes = [IsCandidate]

    def post(self, request):

        file = request.FILES.get('resume')

        if not file:
            return Response({
                "error": "Resume file required"
            }, status=400)

        try:    

            text = extract_resume_text(file)
            structured_data = build_resume_json(text)

        except Exception as e:

            LoggingService().create_error_log("ResumeParserAPIView",str(e))  

            return Response({"error":"Unable to parse resume"},status=400)

        return Response({
            "parsed_text": text,
            "structured_data":structured_data
        })