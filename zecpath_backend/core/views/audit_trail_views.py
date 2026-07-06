from core.views.base_viewset import (BaseViewSet)

from core.models import (AuditTrail)

from core.serializers.audit_trail_serializer import (AuditTrailSerializer)

from core.permissions import IsAdmin


class AuditTrailViewSet(BaseViewSet):

    queryset = (AuditTrail.objects.select_related("user").order_by("-created_at"))

    serializer_class = (AuditTrailSerializer)

    permission_classes = [IsAdmin]