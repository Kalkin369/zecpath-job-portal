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

        except Application.DoesNotExist:

            return Response(
                {
                    "error":
                    "Application not found"
                },
                status=404
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