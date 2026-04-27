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





class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.select_related('job', 'candidate')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['job','title']
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

        #  Resume logic
        resume = serializer.validated_data.get('resume')

        if not resume:
            if not candidate.resume:
                raise ValidationError("No resume provided")
            serializer.save(candidate=candidate, resume=candidate.resume)
        else:
            serializer.save(candidate=candidate)



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