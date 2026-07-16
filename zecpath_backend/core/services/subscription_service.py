from django.utils import timezone

from core.models import (
    UserSubscription
)


class SubscriptionService:

    def has_ai_access(
        self,
        employer
    ):

        subscription = (
            UserSubscription.objects.filter(
                employer=employer,
                is_active=True,
                end_date__gte=timezone.now().date()
            ).select_related(
                'plan'
            ).first()
        )

        if not subscription:
            return False

        return (
            subscription.plan.ai_enabled
        )