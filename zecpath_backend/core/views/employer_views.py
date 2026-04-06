from rest_framework import viewsets
from core.models.employer import Employer
from core.serializers.employer_serializer import EmployerSerializer



class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
