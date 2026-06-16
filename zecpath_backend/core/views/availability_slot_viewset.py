from rest_framework.permissions import (
    IsAuthenticated
)

from core.models import (
    AvailabilitySlot
)

from core.serializers.availability_slot_serializer import (
    AvailabilitySlotSerializer
)

from core.views.base_viewset import (
    BaseViewSet
)


class AvailabilitySlotViewSet(
    BaseViewSet
):

    queryset = (
        AvailabilitySlot.objects.all()
    )

    serializer_class = (
        AvailabilitySlotSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]