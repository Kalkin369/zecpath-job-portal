from django.db import models

class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10,decimal_places=2)

    duration_days = models.IntegerField()

    max_job_posts = models.IntegerField()

    ai_enabled = models.BooleanField(default=False)

    analytics_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name