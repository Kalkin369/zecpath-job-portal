from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models.ai_call import AICall
from core.serializers.ai_call_serializer import(AICallSerializer)

class AICallViewSet(viewsets.ModelViewSet):

    queryset = AICall.objects.all().order_by('-created_at')

    serializer_class = AICallSerializer

    permission_classes = [IsAuthenticated]