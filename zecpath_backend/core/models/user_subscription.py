from django.db import models

from .employer import Employer
from .subscription_plan import SubscriptionPlan


class UserSubscription(models.Model):

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):

        return f"{self.employer} - {self.plan}"
