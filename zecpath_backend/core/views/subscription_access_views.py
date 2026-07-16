from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsEmployer

from core.services.subscription_service import (
    SubscriptionService
)

from core.models import UserSubscription


class SubscriptionAccessAPIView(
    APIView
):

    permission_classes = [
        IsEmployer
    ]

    def get(
        self,
        request
    ):

        employer = request.user.employer

        subscription = (
            UserSubscription.objects.select_related(
                "plan"
            ).filter(
                employer=employer,
                is_active=True
            ).first()
        )

        if not subscription:

            return Response(
                {
                    "message":
                    "No active subscription"
                }
            )

        return Response(

            {
                "subscription":
                subscription.plan.name,

                "active":
                subscription.is_active,

                "ai_enabled":
                SubscriptionService().has_ai_access(
                    employer
                ),

                "analytics_enabled":
                subscription.plan.analytics_enabled,

                "max_job_posts":
                subscription.plan.max_job_posts,

                "expires_on":
                subscription.end_date
            }
        )