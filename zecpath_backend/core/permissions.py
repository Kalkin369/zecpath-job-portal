from rest_framework.permissions import BasePermission

from core.services.subscription_service import SubscriptionService


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "employer")


class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "candidate")


class IsEmployerOrAdmin(BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, "employer") or request.user.role == "admin"


class HasActiveSubscription(BasePermission):

    message = "An active subscription is required."

    def has_permission(self, request, view):

        if not hasattr(request.user, "employer"):
            return False

        employer = request.user.employer

        return SubscriptionService().has_active_subscription(employer)


class CanPostJob(BasePermission):

    message = "Your job posting limit has been reached."

    def has_permission(self, request, view):

        if not hasattr(request.user, "employer"):
            return False

        employer = request.user.employer

        return SubscriptionService().can_post_job(employer)


class CanUseAI(BasePermission):

    message = "Upgrade your subscription to access AI features."

    def has_permission(self, request, view):

        if not hasattr(request.user, "employer"):
            return False

        employer = request.user.employer

        return SubscriptionService().has_ai_access(employer)


class CanViewCandidates(BasePermission):

    message = "Candidate access limit reached."

    def has_permission(self, request, view):

        if not hasattr(request.user, "employer"):
            return False

        employer = request.user.employer

        current_access_count = getattr(request, "candidate_access_count", 0)

        return SubscriptionService().can_access_candidates(
            employer, current_access_count
        )


class CanUseAnalytics(BasePermission):

    message = "Upgrade your subscription to access analytics."

    def has_permission(self, request, view):

        # Admin bypass
        if request.user.is_staff:
            return True

        if not hasattr(request.user, "employer"):
            return False

        return SubscriptionService().has_analytics_access(request.user.employer)
