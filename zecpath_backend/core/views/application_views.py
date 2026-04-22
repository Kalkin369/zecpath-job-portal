from core.views.base_viewset import BaseViewSet
from core.models.application import Application
from core.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCandidate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter




class ApplicationViewSet(BaseViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['job','title']
    orderinig = ['created_at']

    def get_permissions(self):
        if self.action =='create':
            return [IsAuthenticated(),IsCandidate()]
        return [IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.select_related('job','candidate')
        
    