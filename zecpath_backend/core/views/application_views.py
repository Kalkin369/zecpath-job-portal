from core.views.base_viewset import BaseViewSet
from core.models.application import Application
from core.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCandidate
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


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

        if hasattr(user, 'candidate'):
            return self.queryset.filter(candidate=user.candidate)

        return Application.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'candidate'):
            raise ValidationError("Only candidates can apply")

        candidate = user.candidate
        job = serializer.validated_data.get('job')

        # ❌ Check job status
        if job.status != 'active':
            raise ValidationError("Cannot apply to inactive job")

        # ❌ Prevent duplicate
        if Application.objects.filter(candidate=candidate, job=job).exists():
            raise ValidationError("Already applied to this job")

        # ✅ Resume logic
        resume = serializer.validated_data.get('resume')

        if not resume:
            if not candidate.resume:
                raise ValidationError("No resume provided")
            serializer.save(candidate=candidate, resume=candidate.resume)
        else:
            serializer.save(candidate=candidate)