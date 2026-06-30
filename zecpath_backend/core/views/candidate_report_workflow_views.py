from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from core.models import (
    Application
)

from core.services.candidate_report_service import (
    CandidateReportService
)

from core.serializers.candidate_report_serializer import (
    CandidateReportSerializer
)

from core.services.logging_service import (LoggingService)

class GenerateReportAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

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
                Application.objects.get(
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

            LoggingService().create_error_log(
                "GenerateReportAPIView",
                str(e)
            )

            return Response(
                {
                    "error":
                    "Failed to generate report"
                },
                status=500
            )