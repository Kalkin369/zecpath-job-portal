from datetime import timedelta

from django.db.models import Count,Q
from django.utils import timezone

from core.models import Application


class RecruiterAnalyticsService:

    def get_applications(
        self,
        request_user
    ):

        if hasattr(request_user, "employer"):

            return (
                Application.objects.filter(
                    job__employer=request_user.employer
                )
            )

        return (
            Application.objects.all()
        )

    def get_funnel_metrics(
        self,
        request_user
    ):

        applications = (
            self.get_applications(request_user)
        )

        return {

            "applied":
            applications.filter(
                status='applied'
            ).count(),

            "shortlisted":
            applications.filter(
                status='shortlisted'
            ).count(),

            "interview":
            applications.filter(
                status='interview'
            ).count(),

            "selected":
            applications.filter(
                status='selected'
            ).count(),

            "rejected":
            applications.filter(
                status='rejected'
            ).count()
        }

    def get_conversion_rates(
        self,
        request_user
    ):

        applications = (
            self.get_applications(request_user)
        )

        applied = (
            applications.count()
        )

        shortlisted = (
            applications.filter(
                status='shortlisted'
            ).count()
        )

        interview = (
            applications.filter(
                status='interview'
            ).count()
        )

        selected = (
            applications.filter(
                status='selected'
            ).count()
        )

        return {

            "shortlist_rate":
            round(
                (
                    shortlisted / applied * 100
                ),
                2
            ) if applied else 0,

            "interview_rate":
            round(
                (
                    interview / applied * 100
                ),
                2
            ) if applied else 0,

            "selection_rate":
            round(
                (
                    selected / applied * 100
                ),
                2
            ) if applied else 0
        }

    def get_job_performance(
        self,
        request_user
    ):

        applications = (
            self.get_applications(request_user)
        )

        return list(

            applications

            .values(
                'job__title'
            )

            .annotate(
                applications=Count('id')
            )

            .order_by(
                '-applications'
            )
        )

    def get_time_based_stats(
        self,
        request_user
    ):

        applications = (
            self.get_applications(request_user)
        )

        now = (
            timezone.now()
        )

        last_7_days = (
            now - timedelta(days=7)
        )

        last_30_days = (
            now - timedelta(days=30)
        )

        return {

            "last_7_days":
            applications.filter(
                applied_at__gte=last_7_days
            ).count(),

            "last_30_days":
            applications.filter(
                applied_at__gte=last_30_days
            ).count()
        }

    

    def get_job_status_summary(
        self,
        employer,
        job_id
    ):

        applications = Application.objects.filter(
            job_id=job_id,
            job__employer=employer
        )

        return applications.aggregate(

            applied=Count(
                "id",
                filter=Q(status="applied")
            ),

            shortlisted=Count(
                "id",
                filter=Q(status="shortlisted")
            ),

            rejected=Count(
                "id",
                filter=Q(status="rejected")
            ),

            selected=Count(
                "id",
                filter=Q(status="selected")
            )
        )