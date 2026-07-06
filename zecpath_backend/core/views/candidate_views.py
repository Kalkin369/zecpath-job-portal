from core.views.base_viewset import BaseViewSet
from core.models.candidate import Candidate
from core.serializers.candidate_serializer import CandidateSerializer
from core.permissions import IsCandidate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


class CandidateViewSet(BaseViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsCandidate]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['experience']
    search_fields = ['skills','qualification']
    ordering_fields = ['experience']


    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


