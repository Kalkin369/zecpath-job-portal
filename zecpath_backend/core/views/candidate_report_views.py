from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)

from core.models import CandidateReport
from core.permissions import IsEmployerOrAdmin
from core.serializers.candidate_report_serializer import \
    CandidateReportSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Candidate Reports"])
@extend_schema_view(
    list=extend_schema(
        summary="List Candidate Reports",
        description="Retrieve candidate interview reports. Employers see reports for their own candidates, while admins can view all reports.",
        responses={
            200: CandidateReportSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Candidate Report",
        description="Retrieve a candidate report by ID.",
        responses={
            200: CandidateReportSerializer,
            404: OpenApiResponse(description="Candidate report not found."),
        },
    ),
    create=extend_schema(
        summary="Create Candidate Report",
        description="Create a candidate report manually (development/testing).",
        request=CandidateReportSerializer,
        responses={
            201: CandidateReportSerializer,
            400: OpenApiResponse(description="Validation error."),
        },
    ),
    update=extend_schema(
        summary="Update Candidate Report",
        description="Update a candidate report.",
        request=CandidateReportSerializer,
        responses={
            200: CandidateReportSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially Update Candidate Report",
        description="Update selected fields of a candidate report.",
        request=CandidateReportSerializer,
        responses={
            200: CandidateReportSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Candidate Report",
        description="Delete a candidate report.",
        responses={
            204: OpenApiResponse(description="Candidate report deleted."),
        },
    ),
)
class CandidateReportViewSet(BaseViewSet):

    serializer_class = CandidateReportSerializer

    permission_classes = [IsEmployerOrAdmin]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return CandidateReport.objects.none()

        if self.request.user.role == "admin":

            return CandidateReport.objects.all().order_by("-created_at")

        return CandidateReport.objects.filter(
            application__job__employer=self.request.user.employer
        ).order_by("-created_at")
