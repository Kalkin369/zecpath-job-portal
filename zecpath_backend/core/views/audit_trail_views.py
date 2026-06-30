from core.views.base_viewset import (
    BaseViewSet
)

from core.models import (
    AuditTrail
)

from core.serializers.audit_trail_serializer import (
    AuditTrailSerializer
)

from rest_framework.permissions import (
    IsAuthenticated
)


class AuditTrailViewSet(
    BaseViewSet
):

    queryset = (
        AuditTrail.objects.all()
    )

    serializer_class = (
        AuditTrailSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]