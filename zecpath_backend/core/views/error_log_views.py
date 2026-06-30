from core.views.base_viewset import (
    BaseViewSet
)

from core.models import (
    ErrorLog
)

from core.serializers.error_log_serializer import (ErrorLogSerializer)

from rest_framework.permissions import (
    IsAuthenticated
)


class ErrorLogViewSet(
    BaseViewSet
):

    queryset = (
        ErrorLog.objects.all()
    )

    serializer_class = (
        ErrorLogSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]