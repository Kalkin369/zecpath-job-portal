from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from rest_framework.exceptions import ValidationError

from core.models.saved_job import SavedJob
from core.permissions import IsCandidate
from core.serializers.saved_job_serializer import SavedJobSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Saved Jobs"])
@extend_schema_view(
    list=extend_schema(
        summary="List Saved Jobs",
        description="Retrieve all jobs saved by the authenticated candidate.",
        responses={
            200: SavedJobSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Saved Job",
        description="Retrieve a saved job by ID.",
        responses={
            200: SavedJobSerializer,
            404: OpenApiResponse(description="Saved job not found."),
        },
    ),
    create=extend_schema(
        summary="Save Job",
        description="Save a job to the authenticated candidate's saved jobs list.",
        request=SavedJobSerializer,
        responses={
            201: SavedJobSerializer,
            400: OpenApiResponse(description="Job already saved or validation error."),
        },
    ),
    update=extend_schema(
        summary="Update Saved Job",
        description="Update a saved job entry.",
        request=SavedJobSerializer,
        responses={
            200: SavedJobSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially Update Saved Job",
        description="Partially update a saved job entry.",
        request=SavedJobSerializer,
        responses={
            200: SavedJobSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Remove Saved Job",
        description="Remove a job from the authenticated candidate's saved jobs.",
        responses={
            204: OpenApiResponse(description="Saved job removed successfully."),
        },
    ),
)
class SavedJobViewSet(BaseViewSet):

    queryset = SavedJob.objects.select_related("candidate", "job")

    serializer_class = SavedJobSerializer

    permission_classes = [IsCandidate]

    def get_queryset(self):

        return self.queryset.filter(candidate=self.request.user.candidate)

    def perform_create(self, serializer):

        candidate = self.request.user.candidate

        job = serializer.validated_data.get("job")

        if SavedJob.objects.filter(candidate=candidate, job=job).exists():

            raise ValidationError({"job": "Job already saved."})

        serializer.save(candidate=candidate)
