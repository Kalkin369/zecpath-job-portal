from django.db.models import Avg

from core.models import (
    Application,
    Job
)

from core.services.recruiter_analytics_service import (
    RecruiterAnalyticsService
)

from core.services.candidate_report_service import (
    CandidateReportService
)


class PremiumRecruiterService:

    def __init__(self):

        self.analytics_service = RecruiterAnalyticsService()

        self.report_service = CandidateReportService()

    def get_candidate_ranking(
        self,
        employer
    ):

        applications = (
            Application.objects.filter(
                job__employer=employer
            )
            .select_related(
                "candidate__user",
                "job"
            )
        )

        ranking = []

        for application in applications:

            ai_score = (
                self.report_service.calculate_ai_score(
                    application
                )
            )

            final_score = round(
                (
                    application.ats_score * 0.7
                ) +
                (
                    ai_score * 0.3
                ),
                2
            )

            ranking.append({

                "candidate":
                application.candidate.user.full_name,

                "job":
                application.job.title,

                "ats_score":
                application.ats_score,

                "ai_score":
                round(ai_score, 2),

                "final_score":
                final_score,

                "status":
                application.status
            })

        ranking.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranking

    def get_hiring_efficiency(
        self,
        employer
    ):

        applications = (
            Application.objects.filter(
                job__employer=employer
            )
        )

        jobs = Job.objects.filter(
            employer=employer
        )

        total_jobs = jobs.count()

        total_applications = applications.count()

        selected = applications.filter(
            status="selected"
        ).count()

        avg_ats = (
            applications.aggregate(
                avg=Avg("ats_score")
            )["avg"] or 0
        )

        avg_ai = 0

        if total_applications:

            total_ai = 0

            for application in applications:

                total_ai += (
                    self.report_service.calculate_ai_score(
                        application
                    )
                )

            avg_ai = round(
                total_ai / total_applications,
                2
            )

        hiring_rate = round(
            (
                selected / total_applications
            ) * 100,
            2
        ) if total_applications else 0

        return {

            "total_jobs":
            total_jobs,

            "total_applications":
            total_applications,

            "selected_candidates":
            selected,

            "average_ats_score":
            round(avg_ats, 2),

            "average_ai_score":
            avg_ai,

            "hiring_success_rate":
            hiring_rate
        }

    def get_candidate_predictions(
        self,
        employer
    ):

        applications = (
            Application.objects.filter(
                job__employer=employer
            )
            .select_related(
                "candidate__user"
            )
        )

        predictions = []

        for application in applications:

            ai_score = (
                self.report_service.calculate_ai_score(
                    application
                )
            )

            ats = application.ats_score

            if ats >= 90 and ai_score >= 90:

                prediction = "High"

            elif ats >= 70 and ai_score >= 70:

                prediction = "Medium"

            else:

                prediction = "Low"

            predictions.append({

                "candidate":
                application.candidate.user.full_name,

                "ats_score":
                ats,

                "ai_score":
                round(ai_score, 2),

                "success_prediction":
                prediction
            })

        return predictions

    def get_dashboard(
        self,
        employer
    ):

        return {

            "ranking":
            self.get_candidate_ranking(
                employer
            )[:5],

            "hiring_efficiency":
            self.get_hiring_efficiency(
                employer
            ),

            "predictions":
            self.get_candidate_predictions(
                employer
            )[:5]
        }