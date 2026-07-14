from django.db import models


class AvailabilitySlot(models.Model):
    employer = models.ForeignKey("Employer",on_delete=models.CASCADE,related_name="availability_slots")

    role = models.CharField(max_length=100)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role} - {self.employer.company_name}"