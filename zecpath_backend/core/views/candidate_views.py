from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter
)
from core.models.candidate import Candidate
from core.permissions import IsCandidate
from core.serializers.candidate_serializer import CandidateSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Candidates"])
@extend_schema_view(
    list=extend_schema(
        summary="List Candidates",
        description="Retrieve the authenticated candidate profile.",
        responses={
            200: CandidateSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Candidate",
        description="Retrieve a candidate profile.",
        responses={
            200: CandidateSerializer,
            404: OpenApiResponse(description="Candidate not found"),
        },
    ),
    create=extend_schema(
        summary="Create Candidate Profile",
        description="Create a candidate profile for the authenticated user.",
        request=CandidateSerializer,
        responses={
            201: CandidateSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    update=extend_schema(
        summary="Update Candidate Profile",
        description="Update the authenticated candidate profile.",
        request=CandidateSerializer,
        responses={
            200: CandidateSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially Update Candidate Profile",
        description="Update selected fields of the authenticated candidate profile.",
        request=CandidateSerializer,
        responses={
            200: CandidateSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Candidate Profile",
        description="Delete the authenticated candidate profile.",
        responses={
            204: OpenApiResponse(description="Candidate deleted"),
        },
    ),
)
class CandidateViewSet(BaseViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsCandidate]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["experience"]
    search_fields = ["skills", "qualification"]
    ordering_fields = ["experience"]

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
