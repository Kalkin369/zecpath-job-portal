from core.views.base_viewset import BaseViewSet
from core.models.application import Application
from core.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCandidate
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError

from core.models.application_log import ApplicationLog
from core.services.ats_service import calculate_score
from core.services.resume_parser_service import extract_resume_text



class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.select_related('job', 'candidate')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['candidate__user__email','job__title']
    orderinig = ['applied_at']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCandidate()]
        return [IsAuthenticated()]

    def get_queryset(self):
       user = self.request.user

    # Candidate → see own applications
       if hasattr(user, 'candidate'):
        return self.queryset.filter(candidate=user.candidate)

    # Employer → see applications for their jobs
       if hasattr(user, 'employer'):
        return self.queryset.filter(job__employer=user.employer)

       return Application.objects.none()

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
        score = calculate_score(resume_text, job)

        #  Save
        serializer.save(candidate=candidate, resume=resume, ats_score=score)

# Update Status
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        user = request.user

    #  Only employer allowed
        if not hasattr(user, 'employer'):
          raise PermissionDenied("Only employers can update status")

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

        
        ApplicationLog.objects.create(
            application=application,
            old_status=old_status,
            new_status=new_status
        )

        return Response({"message": "Status updated"}) 

#Applicants for a Job
    @action(detail=False, methods=['get'], url_path='job/(?P<job_id>[^/.]+)/applicants')
    def job_applicants(self, request, job_id=None):
        user = request.user

        if not hasattr(user, 'employer'):
          return Response({"error": "Only employers allowed"}, status=403)

        applications = self.queryset.filter(
            job_id=job_id,
            job__employer=user.employer
        ).order_by('-ats_score')

        # pagination
        page = self.paginate_queryset(applications)

        if page is not None:
           serializer = self.get_serializer(page,many=True)
           return self.get_paginated_response(serializer.data)


        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)       
    
# Analytics APIs
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        user = request.user

        if not hasattr(user, 'employer'):
            return Response({"error": "Not allowed"}, status=403)

        apps = self.queryset.filter(job__employer=user.employer)

        total = apps.count()
        shortlisted = apps.filter(status='shortlisted').count()

        ratio = (shortlisted / total * 100) if total > 0 else 0

        return Response({
            "total_applications": total,
            "shortlisted": shortlisted,
            "shortlist_ratio": round(ratio, 2)
        })
    
#Status wise counts per job
    @action(detail=True, methods=['get'])
    def status_summary(self, request, pk=None):
        job_id = pk
        user = request.user

        if not hasattr(user, 'employer'):
            return Response({"error": "Not allowed"}, status=403)

        applications = Application.objects.filter(
            job_id=job_id,
            job__employer=user.employer
        )

        return Response({
            "applied": applications.filter(status='applied').count(),
            "shortlisted": applications.filter(status='shortlisted').count(),
            "rejected": applications.filter(status='rejected').count(),
            "selected": applications.filter(status='selected').count(),
        }) 

#Timeline view
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):

        application = self.get_object()

        if application.candidate != request.user.candidate:
           return Response({"error":"Not allowed"},status=403) 

        logs = application.logs.all().order_by('changed_at')

        data = [
            {
                "old_status": log.old_status,
                "new_status": log.new_status,
                "changed_at": log.changed_at
            }
            for log in logs
        ]

        return Response(data)   