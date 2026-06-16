from django.utils import timezone

from core.models import (InterviewReminder)

from datetime import timedelta


class ReminderService:

    def get_pending_reminders(
        self
    ):

        return (
            InterviewReminder.objects.filter(
                status='pending',
                scheduled_for__lte=
                timezone.now()
            )
        )
    

    def create_reminders(self,schedule):

        # 24 Hours Reminder

        InterviewReminder.objects.create(
            schedule=schedule,
            reminder_type='24_hour',
            scheduled_for=(
                schedule.scheduled_at -
                timedelta(hours=24)
            )
        )

        # 1 Hour Reminder

        InterviewReminder.objects.create(
            schedule=schedule,
            reminder_type='1_hour',
            scheduled_for=(
                schedule.scheduled_at -
                timedelta(hours=1)
            )
        )    