
from core.permissions import IsEmployer

from core.models import (AvailabilitySlot)

from core.serializers.availability_slot_serializer import (AvailabilitySlotSerializer)

from core.views.base_viewset import (BaseViewSet)


class AvailabilitySlotViewSet(BaseViewSet):

    serializer_class = (AvailabilitySlotSerializer)

    permission_classes = [IsEmployer]

    def get_queryset(self):
        return AvailabilitySlot.objects.filter(employer=self.request.user.employer)