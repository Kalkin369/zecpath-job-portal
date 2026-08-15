from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view
)

from core.models import InterviewReminder
from core.permissions import IsEmployer
from core.serializers.interview_reminder_serializer import \
    InterviewReminderSerializer
from core.views.base_viewset import BaseViewSet


@extend_schema(tags=["Interview Scheduling"])
@extend_schema_view(
    list=extend_schema(
        summary="List Interview Reminders",
        description="Retrieve interview reminders.",
        responses={
            200: InterviewReminderSerializer(many=True),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Interview Reminder",
        description="Retrieve an interview reminder.",
        responses={
            200: InterviewReminderSerializer,
            404: OpenApiResponse(description="Interview reminder not found."),
        },
    ),
    create=extend_schema(
        summary="Create Interview Reminder",
        description="Create a new interview reminder.",
        request=InterviewReminderSerializer,
        responses={
            201: InterviewReminderSerializer,
        },
    ),
    update=extend_schema(
        summary="Update Interview Reminder",
        request=InterviewReminderSerializer,
        responses={
            200: InterviewReminderSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partially Update Interview Reminder",
        request=InterviewReminderSerializer,
        responses={
            200: InterviewReminderSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Interview Reminder",
        responses={
            204: OpenApiResponse(description="Interview reminder deleted."),
        },
    ),
)
class InterviewReminderViewSet(BaseViewSet):

    serializer_class = InterviewReminderSerializer

    permission_classes = [IsEmployer]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return InterviewReminder.objects.none()

        return InterviewReminder.objects.filter(
            schedule__application__job__employer=self.request.user.employer
        ).order_by("-id")
