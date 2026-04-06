from rest_framework import viewsets
from core.models.job import Job
from core.serializers.job_serializer import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer