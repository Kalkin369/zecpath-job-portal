from core.views.base_viewset import BaseViewSet
from core.models.job import Job
from core.serializers.job_serializer import JobSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsEmployer

class JobViewSet(BaseViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(),IsEmployer()]
        return [IsAuthenticated()]
    