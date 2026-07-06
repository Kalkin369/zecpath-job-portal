from rest_framework.views import APIView
from rest_framework.response import Response

from core.services.logging_service import (LoggingService)
from core.permissions import IsAdmin
from core.views.base_viewset import (BaseViewSet)
from core.models import (SecurityLog)
from core.serializers.security_log_serializer import (SecurityLogSerializer)


class SecurityTestAPIView(APIView):

    def get(self,request):

        LoggingService().create_security_log(
            request.META.get(
                'REMOTE_ADDR',
                'Unknown'
            ),
            "Unauthorized Access Attempt"
        )

        return Response(
            {
                "message":
                "Security Log Created"
            }
        )
    
class SecurityLogViewSet(BaseViewSet):

    queryset = (SecurityLog.objects.all().order_by('-created_at'))

    serializer_class = (SecurityLogSerializer)

    permission_classes = [IsAdmin]    