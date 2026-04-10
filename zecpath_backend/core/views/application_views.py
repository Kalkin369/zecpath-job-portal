from rest_framework import viewsets
from core.models.application import Application
from core.serializers.application_serializer import ApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsCandidate




class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.action =='create':
            return [IsAuthenticated(),IsCandidate()]
        return [IsAuthenticated]
        
    