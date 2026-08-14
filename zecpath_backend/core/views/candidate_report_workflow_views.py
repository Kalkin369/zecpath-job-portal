from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsAdmin
from core.models import (Application)

from core.services.candidate_report_service import (CandidateReportService)

from core.serializers.candidate_report_serializer import (CandidateReportSerializer)

from core.services.logging_service import (LoggingService)

from drf_spectacular.utils import extend_schema,OpenApiResponse,inline_serializer
from rest_framework import serializers
from core.utils.error_handler import handle_exception

@extend_schema(
    tags=["Candidate Reports"],
    summary="Generate Candidate Report",
    description=(
        "Generate a complete interview report for a candidate "
        "based on their application, AI interview, answers, and evaluations."
    ),
    request=inline_serializer(name="GenerateReportRequest",fields={"application_id":serializers.IntegerField()}),
    responses={
        200: CandidateReportSerializer,
        400: OpenApiResponse(
            description="Application ID is required."
        ),
        404: OpenApiResponse(
            description="Application not found."
        ),
        500: OpenApiResponse(
            description="Failed to generate report."
        ),
    },
)


class GenerateReportAPIView(APIView):

    permission_classes = [IsAdmin]

    def post(self,request):

        application_id = (
            request.data.get(
                'application_id'
            )
        )

        if not application_id:

            return Response(
                {
                    "error":
                    "application_id is required"
                },
                status=400
            )

        try:

            application = (
                Application.objects.select_related("candidate","job").get(
                    id=application_id
                )
            )

            report = (
                CandidateReportService()
                .generate_report(
                    application
                )
            )

            serializer = (
                CandidateReportSerializer(
                    report
                )
            )

            return Response(
                serializer.data
            )

        except Application.DoesNotExist:

            LoggingService().create_error_log(
                "GenerateReportAPIView",
                f"Application {application_id} not found"
            )

            return Response(
                {
                    "error":
                    "Application not found"
                },
                status=404
            )

        except Exception as e:

            return handle_exception(
                "GenerateReportAPIView",e,"Failed to generate report"
            )
            