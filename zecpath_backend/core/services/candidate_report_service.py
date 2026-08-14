from core.models import (
    AnswerEvaluation,
    CandidateReport
)


class CandidateReportService:

    def calculate_ai_score(
        self,
        application
    ):

        evaluations = (AnswerEvaluation.objects.filter(
            answer__question__session__ai_call__application=application
            )
        )

        total_score = sum(
            evaluation.total_score
            for evaluation in evaluations
        )

        count = evaluations.count()

        return (
            total_score / count
            if count else 0
        )

    def generate_report(
        self,
        application,
    ):

        ats_score = (
            application.ats_score
        )

        ai_score = (
            self.calculate_ai_score(
                application
            )
        )

        strengths = []

        risks = []

        # Strengths
        if ats_score >= 70:

            strengths.append(
                "Strong ATS profile"
            )

        if ai_score >= 70:

            strengths.append(
                "Strong technical answers"
            )

        # Risks
        if ats_score < 50:

            risks.append(
                "Low ATS score"
            )

        if ai_score < 50:

            risks.append(
                "Low answer quality"
            )

        # Summary
        summary = (
            f"Candidate achieved "
            f"{ai_score:.2f}% AI score "
            f"with ATS score "
            f"{ats_score:.2f}%."
        )

        # Prevent duplicate reports
        report, created = (
            CandidateReport.objects.update_or_create(
                application=application,
                defaults={
                    'ats_score': ats_score,
                    'ai_score': ai_score,
                    'strengths': strengths,
                    'risks': risks,
                    'summary': summary
                }
            )
        )

        return report
