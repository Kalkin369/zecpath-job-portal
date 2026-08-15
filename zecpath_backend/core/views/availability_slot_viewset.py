from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)
from core.models import AvailabilitySlot
from core.permissions import IsEmployer
from core.serializers.availability_slot_serializer import \
    AvailabilitySlotSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Interview Scheduling"])
@extend_schema_view(
    list=extend_schema(
        summary="List Availability Slots",
        description="Retrieve employer availability slots.",
        responses={
            200: AvailabilitySlotSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Availability Slot",
        description="Retrieve an availability slot.",
        responses={
            200: AvailabilitySlotSerializer,
            404: OpenApiResponse(description="Availability slot not found."),
        },
    ),
    create=extend_schema(
        summary="Create Availability Slot",
        description="Create a new interview availability slot.",
        request=AvailabilitySlotSerializer,
        responses={
            201: AvailabilitySlotSerializer,
        },
    ),
    update=extend_schema(
        summary="Update Availability Slot",
        request=AvailabilitySlotSerializer,
        responses={
            200: AvailabilitySlotSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially Update Availability Slot",
        request=AvailabilitySlotSerializer,
        responses={
            200: AvailabilitySlotSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Availability Slot",
        responses={
            204: OpenApiResponse(description="Availability slot deleted."),
        },
    ),
)
class AvailabilitySlotViewSet(BaseViewSet):

    serializer_class = AvailabilitySlotSerializer

    permission_classes = [IsEmployer]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

        return AvailabilitySlot.objects.filter(employer=self.request.user.employer)

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)
