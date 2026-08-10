from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsCandidate

from core.services.resume_parser_service import (extract_resume_text)
from core.services.resume_nlp_service import (build_resume_json)
from core.services.logging_service import LoggingService
from drf_spectacular.utils import extend_schema,OpenApiExample,OpenApiResponse

@extend_schema(
    tags=["Resume Parser"],
    summary="Parse Resume",
    description=(
        "Upload a candidate resume and extract structured information "
        "such as skills, education, experience, and parsed text."
    ),
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "resume": {
                    "type": "string",
                    "format": "binary"
                }
            },
            "required": ["resume"]
        }
    },
    responses={
        200: OpenApiResponse(
            description="Resume parsed successfully."
        ),
        400: OpenApiResponse(
            description="Resume file is missing or parsing failed."
        ),
        403: OpenApiResponse(
            description="Candidate authentication required."
        ),
    },
    examples=[
        OpenApiExample(
            "Successful Response",
            value={
                "parsed_text": "Experienced Python Developer with Django...",
                "structured_data": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+91XXXXXXXXXX",
                    "skills": [
                        "Python",
                        "Django",
                        "REST API"
                    ],
                    "education": [
                        {
                            "degree": "B.Tech"
                        }
                    ],
                    "experience": [
                        {
                            "company": "ABC Pvt Ltd",
                            "years": 3
                        }
                    ]
                }
            },
            response_only=True,
        )
    ],
)

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