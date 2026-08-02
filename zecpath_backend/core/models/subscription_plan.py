from django.db import models


class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=100,db_index=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration_days = models.IntegerField()

    # Maximum active job posts allowed
    max_job_posts = models.IntegerField()

    # Maximum candidate profiles accessible
    max_candidate_access = models.IntegerField(
        default=0
    )

    # Premium AI Features
    ai_enabled = models.BooleanField(
        default=False
    )

    # Premium Analytics Dashboard
    analytics_enabled = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name