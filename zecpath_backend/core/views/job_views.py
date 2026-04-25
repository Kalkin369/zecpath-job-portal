from core.views.base_viewset import BaseViewSet
from core.models.job import Job
from core.serializers.job_serializer import JobSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class JobViewSet(BaseViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['experience','employer']
    search_fields = ['title','description','skills']
    ordering_fields = ['created_at','experience']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(),IsEmployer()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user

        queryset = Job.objects.select_related('employer')

        if user.is_authenticated:
            # Employer see only thier jobs
            if hasattr(user,'employer'):
                return queryset.filter(employer=user.employer)
        
        # Others(candidate/public) see only active jobs
        return queryset.filter(status='active')
    
    def perform_create(self, serializer):
     user = self.request.user

     if not hasattr(user, 'employer'):
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Only employers can create jobs")

     serializer.save(employer=user.employer)
   
   
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        job = self.get_object()

        # Check ownership
        if not hasattr(request.user, 'employer') or job.employer != request.user.employer:
            return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        # Toggle status
        job.status = 'inactive' if job.status == 'active' else 'active'
        job.save()

        return Response({"message": "Job status updated"})