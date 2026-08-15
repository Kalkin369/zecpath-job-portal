from core.models import AvailabilitySlot, InterviewSchedule
from core.services.reminder_service import ReminderService
from core.tasks import send_schedule_email_task


class SchedulingEngineService:

    def get_available_slot(self, role):

        return (
            AvailabilitySlot.objects.filter(role=role, is_booked=False)
            .order_by("start_time")
            .first()
        )

    def schedule_interview(self, application, role):

        slot = self.get_available_slot(role)

        if not slot:
            return None

        # Conflict Resolution

        existing = InterviewSchedule.objects.filter(
            scheduled_at=slot.start_time
        ).exists()

        if existing:
            return None

        schedule = InterviewSchedule.objects.create(
            application=application, scheduled_at=slot.start_time
        )

        ReminderService().create_reminders(schedule)

        slot.is_booked = True
        slot.save()

        send_schedule_email_task.delay(schedule.id)

        return schedule
