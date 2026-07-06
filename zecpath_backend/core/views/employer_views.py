from core.views.base_viewset import BaseViewSet
from core.models.employer import Employer
from core.serializers.employer_serializer import EmployerSerializer
from core.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter


class EmployerViewSet(BaseViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsEmployer]
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['company_name']
    ordering_fields = ['id','user_email']


    def get_queryset(self):
        return (Employer.objects.select_related("user").filter(user=self.request.user))
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
