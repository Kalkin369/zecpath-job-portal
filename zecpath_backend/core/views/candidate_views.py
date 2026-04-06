from rest_framework import viewsets
from core.models.candidate import Candidate
from core.serializers.candidate_serializer import CandidateSerializer



class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

