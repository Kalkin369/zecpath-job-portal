from rest_framework.permissions import (
    IsAuthenticated
)

from core.models import (
    InterviewReminder
)

from core.serializers.interview_reminder_serializer import (
    InterviewReminderSerializer
)

from core.views.base_viewset import (
    BaseViewSet
)


class InterviewReminderViewSet(
    BaseViewSet
):

    queryset = (
        InterviewReminder.objects.all().order_by('-id')
    )

    serializer_class = (
        InterviewReminderSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]