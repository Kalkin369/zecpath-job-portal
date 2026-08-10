from core.permissions import (IsEmployer)

from core.models import (InterviewSchedule)

from core.serializers.interview_schedule_serializer import (InterviewScheduleSerializer)

from core.views.base_viewset import (BaseViewSet)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

@extend_schema(
    tags=["Interview Scheduling"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List Interview Schedules",
        description="Retrieve interview schedules.",
        responses={
            200: InterviewScheduleSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Interview Schedule",
        description="Retrieve an interview schedule.",
        responses={
            200: InterviewScheduleSerializer,
            404: OpenApiResponse(description="Interview schedule not found."),
        },
    ),

    create=extend_schema(
        summary="Create Interview Schedule",
        description="Create a new interview schedule.",
        request=InterviewScheduleSerializer,
        responses={
            201: InterviewScheduleSerializer,
        },
    ),

    update=extend_schema(
        summary="Update Interview Schedule",
        request=InterviewScheduleSerializer,
        responses={
            200: InterviewScheduleSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially Update Interview Schedule",
        request=InterviewScheduleSerializer,
        responses={
            200: InterviewScheduleSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete Interview Schedule",
        responses={
            204: OpenApiResponse(description="Interview schedule deleted."),
        },
    ),
)

class InterviewScheduleViewSet(BaseViewSet):

    serializer_class = (InterviewScheduleSerializer)

    permission_classes = [IsEmployer]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return InterviewSchedule.objects.none()

        return (
            InterviewSchedule.objects.filter(
                application__job__employer=self.request.user.employer
            )
        )