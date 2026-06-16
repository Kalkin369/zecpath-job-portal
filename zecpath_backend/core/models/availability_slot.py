from django.db import models


class AvailabilitySlot(models.Model):

    role = models.CharField(
        max_length=100
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    is_booked = models.BooleanField(
        default=False
    )