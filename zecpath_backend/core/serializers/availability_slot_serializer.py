from rest_framework import serializers

from core.models import (
    AvailabilitySlot
)


class AvailabilitySlotSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = AvailabilitySlot

        fields = '__all__'