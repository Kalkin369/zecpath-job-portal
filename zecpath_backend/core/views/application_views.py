from rest_framework import viewsets
from core.models.application import Application
from core.serializers.application_serializer import ApplicationSerializer




class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer