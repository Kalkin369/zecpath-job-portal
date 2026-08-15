from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response

from core.models.job import Job
from core.permissions import (
    CanPostJob,
    IsCandidate,
    IsEmployer
)
from core.serializers.job_serializer import JobSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Jobs"])
@extend_schema_view(
    list=extend_schema(
        summary="List Jobs",
        description="Retrieve all active jobs. Employers only see their own jobs.",
        responses={
            200: JobSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Job",
        description="Retrieve a single job by ID.",
        responses={
            200: JobSerializer,
            404: OpenApiResponse(description="Job not found"),
        },
    ),
    create=extend_schema(
        summary="Create Job",
        description="Employer creates a new job posting. Active subscription required.",
        request=JobSerializer,
        responses={
            201: JobSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Permission denied"),
        },
    ),
    update=extend_schema(
        summary="Update Job",
        description="Update an existing job.",
        request=JobSerializer,
        responses={
            200: JobSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially Update Job",
        description="Update selected fields of a job.",
        request=JobSerializer,
        responses={
            200: JobSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Job",
        description="Delete an existing job.",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
        },
    ),
)
class JobViewSet(BaseViewSet):
    queryset = Job.objects.select_related("employer").order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [
        IsAuthenticated
    ]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = [
        "experience",
        "job_type",
        "location"
    ]
    search_fields = [
        "title",
        "skills", 
        "location"
    ]
    ordering_fields = [
        "created_at",
        "experience",
        "salary_min"
    ]

    def get_permissions(self):

        if self.action in ["list", "retrieve", "latest", "featured"]:
            permission_classes = [AllowAny]

        elif self.action == "create":
            permission_classes = [
                IsAuthenticated,
                IsEmployer,
                CanPostJob,
            ]

        elif self.action == "recommended":
            permission_classes = [
                IsAuthenticated,
                IsCandidate,
            ]

        elif self.action == "toggle_status":
            permission_classes = [
                IsAuthenticated,
                IsEmployer,
            ]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset

        # 🔹 Query params (filters)
        min_salary = self.request.query_params.get("min_salary")
        max_salary = self.request.query_params.get("max_salary")

        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)

        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)

        user = self.request.user

        # 🔹 Employer → see own jobs
        if user.is_authenticated and hasattr(user, "employer"):
            return queryset.filter(employer=user.employer)

        # 🔹 Public/Candidate → only active jobs
        return queryset.filter(status="active")

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, "employer"):

            raise PermissionDenied("Only employers can create jobs")

        serializer.save(employer=user.employer)

    @extend_schema(
        summary="Toggle Job Status",
        description="Activate or deactivate a job posting owned by the authenticated employer.",
        responses={
            200: OpenApiResponse(description="Job status updated"),
            403: OpenApiResponse(description="Permission denied"),
        },
    )
    # Toggle status
    @action(detail=True, methods=["post"])
    def toggle_status(self, request, pk=None):
        job = self.get_object()

        # Check ownership
        if (
            not hasattr(request.user, "employer")
            or job.employer != request.user.employer
        ):
            raise PermissionDenied("You cannot modify this job")

        # Toggle status
        job.status = "inactive" if job.status == "active" else "active"
        job.save()

        return Response({"message": "Job status updated"})

    @extend_schema(
        summary="Latest Jobs",
        description="Return the latest 10 active job postings. Results are cached.",
        responses={
            200: JobSerializer(many=True),
        },
    )
    # Latest Jobs
    @action(detail=False, methods=["get"])
    def latest(self, request):

        cached_jobs = cache.get("latest_jobs")

        if cached_jobs:
            return Response(cached_jobs)

        jobs = self.queryset.filter(status="active").order_by("-created_at")[:10]
        serializer = self.get_serializer(jobs, many=True)

        cache.set("latest_jobs", serializer.data, timeout=60)

        return Response(serializer.data)

    @extend_schema(
        summary="Featured Jobs",
        description="Return featured jobs suitable for freshers (experience ≤ 2 years). Cached for performance.",
        responses={
            200: JobSerializer(many=True),
        },
    )
    # Featured Jobs
    @action(detail=False, methods=["get"])
    def featured(self, request):

        cached_jobs = cache.get("featured_jobs")

        if cached_jobs:
            return Response(cached_jobs)

        jobs = self.queryset.filter(status="active", experience__lte=2)[:5]
        serializer = self.get_serializer(jobs, many=True)

        cache.set("featured_jobs", serializer.data, timeout=60)

        return Response(serializer.data)

    @extend_schema(
        summary="Recommended Jobs",
        description="Return jobs matching the authenticated candidate's skills.",
        responses={
            200: JobSerializer(many=True),
            401: OpenApiResponse(description="Authentication required"),
        },
    )
    # Profile based Recommendations
    @action(detail=False, methods=["get"])
    def recommended(self, request):

        user = request.user

        candidate = user.candidate

        skills = candidate.skills.split(",")

        queryset = self.queryset.filter(status="active")

        matched_jobs = []

        for job in queryset:
            job_skills = job.skills.lower()

            for skill in skills:
                if skill.strip().lower() in job_skills:
                    matched_jobs.append(job)
                    break

        serializer = self.get_serializer(matched_jobs, many=True)

        return Response(serializer.data)
