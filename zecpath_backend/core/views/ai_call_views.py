from rest_framework import viewsets
from core.permissions import IsEmployerOrAdmin

from core.models.ai_call import AICall
from core.serializers.ai_call_serializer import(AICallSerializer)

class AICallViewSet(viewsets.ModelViewSet):

    serializer_class = AICallSerializer

    permission_classes = [IsEmployerOrAdmin]

    def get_queryset(self):
        
        if self.request.user.role == "admin":
            return (AICall.objects.all().order_by("-created_at"))
        
        return (AICall.objects.filter(application__job__employer=self.request.user.employer).order_by("-created_at"))