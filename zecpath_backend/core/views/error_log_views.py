from core.views.base_viewset import (BaseViewSet)

from core.models import (ErrorLog)

from core.serializers.error_log_serializer import (ErrorLogSerializer)

from core.permissions import IsAdmin


class ErrorLogViewSet(BaseViewSet):

    queryset = (ErrorLog.objects.all().order_by("-created_at"))

    serializer_class = (ErrorLogSerializer)

    permission_classes = [IsAdmin]