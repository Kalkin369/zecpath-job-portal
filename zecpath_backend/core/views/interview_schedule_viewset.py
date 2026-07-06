from core.permissions import (IsEmployer)

from core.models import (InterviewSchedule)

from core.serializers.interview_schedule_serializer import (InterviewScheduleSerializer)

from core.views.base_viewset import (BaseViewSet)


class InterviewScheduleViewSet(BaseViewSet):

    serializer_class = (InterviewScheduleSerializer)

    permission_classes = [IsEmployer]

    def get_queryset(self):
        return (InterviewSchedule.objects.filter(application__job__employer=self.request.user.employer))