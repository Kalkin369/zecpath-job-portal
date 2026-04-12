from rest_framework import viewsets
from core.models.employer import Employer
from core.serializers.employer_serializer import EmployerSerializer
from rest_framework.permissions import IsAuthenticated


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employer.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
