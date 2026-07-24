from django.db.models import Sum, Count,F
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from core.models import (
    BillingHistory,
    PaymentTransaction,
    UserSubscription
)


class FinanceService:

    def get_transactions(self):

        return (
            PaymentTransaction.objects
            .select_related(
                "subscription",
                "subscription__employer",
                "subscription__plan"
            )
            .order_by("-created_at")
        )

    def get_subscription_history(self):

        return (
            BillingHistory.objects
            .select_related(
                "employer",
                "payment"
            )
            .order_by("-created_at")
        )

    def get_daily_revenue(self):

        return (
            PaymentTransaction.objects
            .filter(
                status="success"
            )
            .annotate(
                day=TruncDate("created_at")
            )
            .values("day")
            .annotate(
                revenue=Sum("amount"),
                transactions=Count("id")
            )
            .order_by("-day")
        )

    def get_monthly_revenue(self):

        return (
            PaymentTransaction.objects
            .filter(
                status="success"
            )
            .annotate(
                month=TruncMonth("created_at")
            )
            .values("month")
            .annotate(
                revenue=Sum("amount"),
                transactions=Count("id")
            )
            .order_by("-month")
        )

    def get_plan_revenue(self):

        return (
            PaymentTransaction.objects
            .filter(status="success")
            .annotate(plan_name=F("subscription__plan__name"))
            .values(
                "plan_name"
            )
            .annotate(
                revenue=Sum("amount"),
                subscriptions=Count("id")
            )
            .order_by("-revenue")
        )

    def get_refund_logs(self):

        return (
            PaymentTransaction.objects
            .filter(
                status__in=[
                    "refund_pending",
                    "refunded"
                ]
            )
            .select_related(
                "subscription",
                "subscription__employer",
                "subscription__plan"
            )
            .order_by("-updated_at")
        )

    def get_payment_failures(self):

        payments = (
            PaymentTransaction.objects
            .filter(status="failed")
            .select_related(
                "subscription",
                "subscription__employer",
                "subscription__plan"
            ).order_by("-updated_at")
        )

        return [
            {
                "payment_id": payment.id,
                "employer": payment.subscription.employer.company_name,
                "plan": payment.subscription.plan.name,
                "amount": payment.amount,
                "gateway": payment.gateway,
                "status": payment.status,
                "created_at": payment.created_at,
            }
            for payment in payments
        ]

    def get_dashboard(self):

        today = timezone.now().date()

        today_revenue = (
            PaymentTransaction.objects
            .filter(
                status="success",
                created_at__date=today
            )
            .aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        total_revenue = (
            PaymentTransaction.objects
            .filter(
                status="success"
            )
            .aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        successful = (
            PaymentTransaction.objects
            .filter(
                status="success"
            )
            .count()
        )

        failed = (
            PaymentTransaction.objects
            .filter(
                status="failed"
            )
            .count()
        )

        refunded = (
            PaymentTransaction.objects
            .filter(
                status="refunded"
            )
            .count()
        )

        active_subscriptions = (
            UserSubscription.objects
            .filter(
                is_active=True
            )
            .count()
        )

        return {

            "today_revenue": today_revenue,

            "total_revenue": total_revenue,

            "successful_transactions": successful,

            "failed_transactions": failed,

            "refunded_transactions": refunded,

            "active_subscriptions": active_subscriptions
        }