from core.views.base_viewset import BaseViewSet
from core.models.application import Application
from core.models.job import Job
from core.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCandidate,IsEmployer,IsAdmin,CanViewCandidates,CanUseAnalytics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from core.models.application_log import ApplicationLog
from core.services.ats_service import calculate_ats_score
from core.services.resume_parser_service import extract_resume_text
from core.services.resume_nlp_service import build_resume_json
from core.services.notification_service import send_application_status_email
from core.services.automation_service import auto_update_application_status
from core.services.recruiter_analytics_service import (RecruiterAnalyticsService)
from core.services.s3_service import S3Service

from django.core.cache import cache
from django.db import transaction

from drf_spectacular.utils import (extend_schema,extend_schema_view,OpenApiResponse,)

@extend_schema(
    tags=["Applications"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List Applications",
        description="Retrieve applications visible to the authenticated user. Candidates see their own applications, while employers see applications for their jobs.",
        responses={200: ApplicationSerializer(many=True)},
    ),

    retrieve=extend_schema(
        summary="Retrieve Application",
        description="Retrieve a single application.",
        responses={
            200: ApplicationSerializer,
            404: OpenApiResponse(description="Application not found"),
        },
    ),

    create=extend_schema(
        summary="Apply for Job",
        description="Candidate submits an application. ATS score is calculated automatically from the uploaded resume.",
        request=ApplicationSerializer,
        responses={
            201: ApplicationSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Permission denied"),
        },
    ),

    update=extend_schema(
        summary="Update Application",
        description="Admin updates an application.",
        request=ApplicationSerializer,
        responses={200: ApplicationSerializer},
    ),

    partial_update=extend_schema(
        summary="Partially Update Application",
        description="Admin partially updates an application.",
        request=ApplicationSerializer,
        responses={200: ApplicationSerializer},
    ),

    destroy=extend_schema(
        summary="Delete Application",
        description="Delete an application.",
        responses={
            204: OpenApiResponse(description="Application deleted"),
        },
    ),
)


class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.select_related('job','job__employer', 'candidate','candidate__user')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['candidate__user__email','job__title']
    ordering = ['applied_at']


    def get_permissions(self):

        if self.action == "create":
           permission_classes = [IsCandidate]

        elif self.action == "job_applicants":
           permission_classes =[IsEmployer]   

        elif self.action == "status_summary":
            permission_classes = [IsEmployer,CanUseAnalytics]

        elif self.action == "update_status":
           permission_classes=[IsEmployer]    

        elif self.action == "timeline":
            permission_classes = [IsAuthenticated]

        elif self.action == "download_resume":
           permission_classes =[IsAuthenticated]    

        elif self.action in [
            "destroy",
            "update",
            "partial_update",
        ]:
            permission_classes = [IsAdmin]

        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]
    

    def get_queryset(self):
       user = self.request.user

    # Candidate → see own applications
       if hasattr(user, 'candidate'):
        return self.queryset.filter(candidate=user.candidate)

    # Employer → see applications for their jobs
       if hasattr(user, 'employer'):
        return self.queryset.filter(job__employer=user.employer)

       return Application.objects.none()
    
    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'candidate'):
            raise ValidationError("Only candidates can apply")

        candidate = user.candidate
        job = serializer.validated_data.get('job')

        #  Check job status
        if job.status != 'active':
            raise ValidationError("Cannot apply to inactive job")

        #  Prevent duplicate
        if Application.objects.filter(candidate=candidate, job=job).exists():
            raise ValidationError("Already applied to this job")

     #   Resume logic
        resume = serializer.validated_data.get('resume')

        #  Case 1: Resume sent in request
        if resume:
          file = resume

        #  Case 2: Use candidate profile resume
        elif candidate.resume and candidate.resume.name:
           file = candidate.resume

        #  Case 3: No resume anywhere
        else:
          raise ValidationError("No resume provided")
        
       
        #  Extract text
        resume_text = extract_resume_text(file)

        #  Calculate ATS score
        structured_resume = build_resume_json(resume_text)

        score_data = calculate_ats_score(structured_resume,job)

        #  Save application
        application = serializer.save(candidate=candidate, resume=file, ats_score=score_data['final_score'])

        # Auto automation
        auto_update_application_status(application)



    @extend_schema(
    summary="Update Application Status",
    description="Employer updates an applicant's status following the allowed workflow (Applied → Shortlisted → Interview → Selected/Rejected).",
    responses={
        200: OpenApiResponse(description="Status updated"),
        400: OpenApiResponse(description="Invalid transition"),
        403: OpenApiResponse(description="Permission denied"),
    },
    )

# Update Status
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        user = request.user


    #  Ownership check
        if application.job.employer != user.employer:
          raise PermissionDenied("You can only manage your job applications")

        new_status = request.data.get('status')

        if not new_status:
          raise ValidationError("Status is required")
        current_status = application.status

    # Same status check
        if new_status == current_status:
           raise ValidationError("Application already in this status")

    #  Allowed transitions
        allowed_transitions = {
         'applied': ['shortlisted', 'rejected'],
         'shortlisted': ['interview', 'rejected'],
         'interview': ['selected', 'rejected'],
         'selected': [],
         'rejected': [],
    }

        

        if new_status not in allowed_transitions[current_status]:
          raise ValidationError(f"Cannot move from {current_status} to {new_status}")
        
    #  Update + Log
        old_status = application.status

        application.status = new_status
        application.save()

        send_application_status_email(application)

        
        ApplicationLog.objects.create(
            application=application,
            old_status=old_status,
            new_status=new_status
        )

        return Response({"message": "Status updated","application_id":application.id,"status":application.status}) 



    @extend_schema(
    summary="Job Applicants",
    description="Return all applicants for a specific job ordered by ATS score.",
    responses={
        200: ApplicationSerializer(many=True),
        403: OpenApiResponse(description="Permission denied"),
    },
    )

#Applicants for a Job
    @action(detail=False, methods=['get'], url_path='job/(?P<job_id>[^/.]+)/applicants')
    def job_applicants(self, request, job_id=None):

        job = get_object_or_404(Job, id=job_id)

        # Permission check
        if job.employer != request.user.employer:
            raise PermissionDenied("You can only view applicants for your own jobs.")

        applications = self.queryset.filter(
            job_id=job_id
        ).order_by('-ats_score')

        # Pagination
        page = self.paginate_queryset(applications)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    
    

    @extend_schema(
    summary="Application Status Summary",
    description="Return status-wise application counts for a job. Cached for performance.",
    responses={
        200: OpenApiResponse(description="Status summary"),
    },
    )

#Status wise counts per job
    @action(detail=False,methods=["get"],url_path=r"job/(?P<job_id>[^/.]+)/status-summary")
    def status_summary(self, request, job_id=None):

        cache_key = f"status_summary_{request.user.employer.id}_{job_id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        service = RecruiterAnalyticsService()

        summary = service.get_job_status_summary(
            request.user.employer,
            job_id
        )

        cache.set(
            cache_key,
            summary,
            timeout=120
        )

        return Response(summary)




    @extend_schema(
    summary="Application Timeline",
    description="Return the complete status change history of an application.",
    responses={
        200: OpenApiResponse(description="Timeline"),
        403: OpenApiResponse(description="Permission denied"),
    },
    )

# Timeline View
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):

        application = self.get_object()

        # Candidate can view only their own application timeline
        if hasattr(request.user, "candidate"):

            if application.candidate != request.user.candidate:
                return Response(
                    {"error": "Not allowed"},
                    status=403
                )

        # Employer can view timelines only for jobs they own
        elif hasattr(request.user, "employer"):

            if application.job.employer != request.user.employer:
                return Response(
                    {"error": "Not allowed"},
                    status=403
                )

        # Any other user is denied
        else:

            return Response(
                {"error": "Not allowed"},
                status=403
            )

        logs = (
            application.logs
            .all()
            .order_by("changed_at")
        )

        data = [
            {
                "old_status": log.old_status,
                "new_status": log.new_status,
                "changed_at": log.changed_at
            }
            for log in logs
        ]

        return Response(data)

    



    @extend_schema(
    summary="Download Resume",
    description="Generate a temporary AWS S3 pre-signed URL for downloading the applicant's resume.",
    responses={
        200: OpenApiResponse(description="Pre-signed download URL"),
        403: OpenApiResponse(description="Permission denied"),
        404: OpenApiResponse(description="Resume not found"),
    },
    )

    @action(detail=True, methods=["get"], url_path="download-resume")
    def download_resume(self, request, pk=None):

        application = self.get_object()

        # Candidate can download only their own resume
        if hasattr(request.user, "candidate"):
            if application.candidate != request.user.candidate:
                raise PermissionDenied("You are not allowed to access this resume.")

        # Employer can download resumes only for jobs they own
        elif hasattr(request.user, "employer"):
            if application.job.employer != request.user.employer:
                raise PermissionDenied("You are not allowed to access this resume.")

        else:
            raise PermissionDenied("Not allowed.")

        if not application.resume:
            raise ValidationError("Resume not found.")

        url = S3Service.generate_presigned_url(
            application.resume.name
        )

        return Response({
            "download_url": url
        })