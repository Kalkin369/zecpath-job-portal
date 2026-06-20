from core.models import (Application)
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta



class RecruiterAnalyticsService:

    def get_funnel_metrics(self):

        applied = (Application.objects.filter(status='applied').count())

        shortlisted = (Application.objects.filter(status='shortlisted').count())

        interview = (Application.objects.filter(status='interview').count())

        selected = (Application.objects.filter(status='selected').count())

        rejected = (Application.objects.filter(status='rejected').count())

        return {
            "applied": applied,
            "shortlisted": shortlisted,
            "interview": interview,
            "selected": selected,
            "rejected": rejected
        }

    def get_conversion_rates(self):

        applied = (Application.objects.count())

        shortlisted = (Application.objects.filter(status='shortlisted').count())

        interview = (Application.objects.filter(status='interview').count())

        selected = (Application.objects.filter(status='selected').count())

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
    
    def get_job_performance(self):

        return list(

            Application.objects
            .values('job__title')

            .annotate(applications=Count('id'))
            
            .order_by('-applications')
        )
    
    def get_time_based_stats(self):

        now = (timezone.now())

        last_7_days = (now -timedelta(days=7))

        last_30_days = (now -timedelta(days=30))

        return {

            "last_7_days":Application.objects.filter(applied_at__gte=last_7_days).count(),

            "last_30_days":Application.objects.filter(applied_at__gte=last_30_days).count()
        }