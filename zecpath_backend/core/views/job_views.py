from core.views.base_viewset import BaseViewSet
from core.models.job import Job
from core.serializers.job_serializer import JobSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

class JobViewSet(BaseViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['experience_required','employer']
    search_fields = ['title','description','required_skills']
    ordering_fields = ['created_at','experience_required']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(),IsEmployer()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return Job.objects.select_related('employer')