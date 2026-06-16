from rest_framework.permissions import (
    IsAuthenticated
)

from core.models import (
    InterviewSchedule
)

from core.serializers.interview_schedule_serializer import (
    InterviewScheduleSerializer
)

from core.views.base_viewset import (
    BaseViewSet
)


class InterviewScheduleViewSet(
    BaseViewSet
):

    queryset = (
        InterviewSchedule.objects.all()
    )

    serializer_class = (
        InterviewScheduleSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]