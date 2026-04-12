from rest_framework import viewsets
from core.models.candidate import Candidate
from core.serializers.candidate_serializer import CandidateSerializer
from rest_framework.permissions import IsAuthenticated


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


