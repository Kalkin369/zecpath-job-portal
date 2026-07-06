from core.permissions import IsEmployer
from core.models import (InterviewReminder)

from core.serializers.interview_reminder_serializer import (InterviewReminderSerializer)

from core.views.base_viewset import (BaseViewSet)


class InterviewReminderViewSet(BaseViewSet):

    serializer_class = (InterviewReminderSerializer)

    permission_classes = [IsEmployer]

    def get_queryset(self):
        return (InterviewReminder.objects.filter(schedule__application__job__employer=self.request.user.employer).order_by("-id"))