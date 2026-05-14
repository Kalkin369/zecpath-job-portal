from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.services.resume_parser_service import (
    extract_resume_text
)


class ResumeParserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        file = request.FILES.get('resume')

        if not file:
            return Response({
                "error": "Resume file required"
            }, status=400)

        text = extract_resume_text(file)

        return Response({
            "parsed_text": text
        })