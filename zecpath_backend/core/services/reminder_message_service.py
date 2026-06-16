class ReminderMessageService:

    def build_email(
        self,
        schedule
    ):

        return (
            f"Reminder: Your interview "
            f"is scheduled for "
            f"{schedule.scheduled_at}"
        )