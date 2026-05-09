from core.views.base_viewset import BaseViewSet
from core.models.saved_job import SavedJob
from core.serializers.saved_job_serializer import SavedJobSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCandidate
from rest_framework.exceptions import ValidationError


class SavedJobViewSet(BaseViewSet):
    queryset = SavedJob.objects.select_related('candidate', 'job')
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        return [IsAuthenticated(), IsCandidate()]

    def get_queryset(self):
        return self.queryset.filter(candidate=self.request.user.candidate)

    def perform_create(self, serializer):

        candidate = self.request.user.candidate
        job = serializer.validated_data.get('job')

        if SavedJob.objects.filter(candidate=candidate, job=job).exists():
            raise ValidationError("Job already saved")

        serializer.save(candidate=candidate)