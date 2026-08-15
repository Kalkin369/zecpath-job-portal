from django.utils import timezone

from core.models import Job, UserSubscription


class SubscriptionService:

    def get_active_subscription(self, employer):
        """
        Returns employer's active subscription.
        """

        return self.deactivate_expired_subscription(employer)

    def has_active_subscription(self, employer):

        return self.get_active_subscription(employer) is not None

    def has_ai_access(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:
            return False

        return subscription.plan.ai_enabled

    def has_analytics_access(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:
            return False

        return subscription.plan.analytics_enabled

    def can_post_job(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:
            return False

        total_jobs = Job.objects.filter(employer=employer, status="active").count()

        return total_jobs < subscription.plan.max_job_posts

    def can_access_candidates(self, employer, current_access_count):

        subscription = self.get_active_subscription(employer)

        if not subscription:
            return False

        return current_access_count < subscription.plan.max_candidate_access

    def get_subscription_status(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:

            return {"active": False, "message": "No active subscription."}

        return {
            "active": True,
            "plan": subscription.plan.name,
            "start_date": subscription.start_date,
            "end_date": subscription.end_date,
            "ai_enabled": (subscription.plan.ai_enabled),
            "analytics_enabled": (subscription.plan.analytics_enabled),
            "max_job_posts": (subscription.plan.max_job_posts),
            "max_candidate_access": (subscription.plan.max_candidate_access),
        }

    def deactivate_expired_subscription(self, employer):
        subscription = (
            UserSubscription.objects.select_related("plan")
            .filter(employer=employer, is_active=True)
            .first()
        )

        if not subscription:
            return None

        if subscription.end_date < timezone.now().date():

            subscription.is_active = False
            subscription.save(update_fields=["is_active"])

            return None

        return subscription

    def get_subscription_features(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:

            return {"active": False}

        return {
            "active": True,
            "ai_enabled": subscription.plan.ai_enabled,
            "analytics_enabled": subscription.plan.analytics_enabled,
            "max_job_posts": subscription.plan.max_job_posts,
            "max_candidate_access": subscription.plan.max_candidate_access,
        }

    def get_subscription_usage(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:

            return {"active": False}

        jobs_used = Job.objects.filter(employer=employer, status="active").count()

        return {
            "active": True,
            "jobs_used": jobs_used,
            "jobs_remaining": max(subscription.plan.max_job_posts - jobs_used, 0),
            # Placeholder until candidate usage tracking is implemented
            "candidate_access_used": 0,
            "candidate_access_remaining": subscription.plan.max_candidate_access,
        }

    def get_subscription_access(self, employer):

        subscription = self.get_active_subscription(employer)

        if not subscription:

            return {"active": False, "message": "No active subscription."}

        jobs_used = Job.objects.filter(employer=employer, status="active").count()

        jobs_remaining = max(subscription.plan.max_job_posts - jobs_used, 0)

        candidate_access_used = 0

        candidate_access_remaining = max(
            subscription.plan.max_candidate_access - candidate_access_used, 0
        )

        return {
            "subscription": subscription.plan.name,
            "active": subscription.is_active,
            "ai_enabled": subscription.plan.ai_enabled,
            "analytics_enabled": subscription.plan.analytics_enabled,
            "max_job_posts": subscription.plan.max_job_posts,
            "jobs_used": jobs_used,
            "jobs_remaining": jobs_remaining,
            "max_candidate_access": subscription.plan.max_candidate_access,
            "candidate_access_used": candidate_access_used,
            "candidate_access_remaining": candidate_access_remaining,
            "start_date": subscription.start_date,
            "expires_on": subscription.end_date,
        }

    def deactivate_all_expired_subscriptions(self):

        today = timezone.now().date()

        expired_subscriptions = UserSubscription.objects.filter(
            is_active=True, end_date__lt=today
        )

        updated_count = expired_subscriptions.update(is_active=False)

        return updated_count
