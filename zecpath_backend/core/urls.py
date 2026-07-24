from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *
from core.views.auth_views import SignupAPI,LoginAPI,RefreshAPI
from core.views.saved_job_views import SavedJobViewSet
from core.views.admin_views import AdminEmployerViewSet,AdminUserViewSet,AdminJobViewSet
from core.views.resume_parser_views import (ResumeParserAPIView)
from core.views.notification_log_views import (NotificationLogViewSet)
from core.views.ai_call_views import (AICallViewSet)
from core.views.ai_interview_session_views import (AIInterviewSessionViewSet)
from core.views.ai_question_views import (AIQuestionViewSet)
from core.views.ai_answer_views import (AIAnswerViewSet)
from core.views.call_log_views import (CallLogViewSet)
from core.views.ai_integration_views import (GenerateQuestionAPIView,TextToSpeechAPIView,SpeechToTextAPIView,TriggerCallAPIView)
from core.views.question_engine_views import(NextQuestionAPIView,SubmitAnswerAPIView)
from core.views.answer_evaluation_views import (EvaluateAnswerAPIView,AnswerEvaluationDetailAPIView)
from core.views.interview_schedule_workflow_views import (ScheduleInterviewAPIView,RescheduleInterviewAPIView)
from core.views.interview_schedule_viewset import (InterviewScheduleViewSet)
from core.views.availability_slot_viewset import (AvailabilitySlotViewSet)
from core.views.interview_reminder_views import (InterviewReminderViewSet)
from core.views.candidate_report_views import (CandidateReportViewSet)
from core.views.candidate_report_workflow_views import (GenerateReportAPIView)
from core.views.recruiter_analytics_views import (RecruiterAnalyticsAPIView)
from core.views.security_log_views import (SecurityTestAPIView,SecurityLogViewSet)
from core.views.audit_trail_views import (AuditTrailViewSet)
from core.views.error_log_views import (ErrorLogViewSet)
from core.views.security_report_views import (SecurityReportAPIView)
from core.views.subscription_plan_views import (SubscriptionPlanViewSet)
from core.views.user_subscription_views import (UserSubscriptionViewSet)
from core.views.payment_transaction_views import (PaymentTransactionViewSet)
from core.views.billing_history_views import (BillingHistoryViewSet)
from core.views.subscription_access_views import (SubscriptionAccessAPIView)
from core.views.create_payment_order_api_view import (CreatePaymentOrderAPIView)
from core.views.verify_payment_api_view import (VerifyPaymentAPIView)
from core.views.payment_test_view import (PaymentTestView)
from core.views.payment_webhook_api_view import (PaymentWebhookAPIView)
from core.views.payment_history_views import (PaymentHistoryAPIView)
from core.views.payment_detail_views import (PaymentDetailAPIView)
from core.views.refund_payment_views import (RefundPaymentAPIView)
from core.views.subscription_access_views import (SubscriptionAccessAPIView)
from core.views.premium_recruiter_views import (CandidateRankingAPIView,HiringEfficiencyAPIView,CandidatePredictionAPIView,PremiumDashboardAPIView)
from core.views.admin_finance_views import (FinanceDashboardAPIView,DailyRevenueAPIView,MonthlyRevenueAPIView,PlanRevenueAPIView,PaymentFailureAPIView)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('employers', EmployerViewSet,basename='employer')
router.register('candidates', CandidateViewSet,basename='candidate')
router.register('jobs', JobViewSet)
router.register('applications', ApplicationViewSet)
router.register('saved-jobs',SavedJobViewSet,basename='saved-jobs')
router.register('admin/employers',AdminEmployerViewSet,basename='admin-employers')
router.register('admin/users',AdminUserViewSet,basename='admin-users')
router.register('admin/jobs',AdminJobViewSet,basename='admin-jobs')
router.register('notification-logs',NotificationLogViewSet,basename='notification-logs')
router.register('ai-calls',AICallViewSet,basename='ai-calls')
router.register('ai-sessions',AIInterviewSessionViewSet,basename='ai-sessions')
router.register('ai-questions',AIQuestionViewSet,basename='ai-questions')
router.register('ai-answers',AIAnswerViewSet,basename='ai-answers')
router.register('call-logs',CallLogViewSet,basename='call-logs')
router.register('interview-schedules',InterviewScheduleViewSet,basename='interview-schedule')
router.register('availability-slots',AvailabilitySlotViewSet,basename='availability-slot')
router.register('interview-reminders',InterviewReminderViewSet,basename='interview-reminders')
router.register('candidate-reports',CandidateReportViewSet,basename='candidate-reports')
router.register('security-logs',SecurityLogViewSet,basename='security-logs')
router.register('audit-trails',AuditTrailViewSet,basename='audit-trails')
router.register('error-logs',ErrorLogViewSet,basename='error-logs')

router.register("subscription-plans",SubscriptionPlanViewSet,basename="subscription-plans")

router.register("user-subscriptions",UserSubscriptionViewSet,basename="user-subscriptions")

router.register("payment-transactions",PaymentTransactionViewSet,basename="payment-transactions")

router.register("billing-history",BillingHistoryViewSet,basename="billing-history")


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    path('auth/refresh/',RefreshAPI.as_view()),
    path('resume-parser/',ResumeParserAPIView.as_view()),
    path('ai/generate-question/',GenerateQuestionAPIView.as_view()),
    path('ai/text-to-speech/',TextToSpeechAPIView.as_view()),
    path('ai/speech-to-text/',SpeechToTextAPIView.as_view()),
    path('ai/trigger-call/',TriggerCallAPIView.as_view()),
    path('question-engine/next-question/',NextQuestionAPIView.as_view()),
    path('question-engine/answer/',SubmitAnswerAPIView.as_view()),
    path('evaluate-answer/',EvaluateAnswerAPIView.as_view(),name='evaluate-answer'),
    path('evaluations/<int:evaluation_id>/',AnswerEvaluationDetailAPIView.as_view(),name='evaluation-detail'),
    path('schedule-interview/',ScheduleInterviewAPIView.as_view()),
    path('reschedule-interview/<int:schedule_id>/',RescheduleInterviewAPIView.as_view()),
    path('generate-report/',GenerateReportAPIView.as_view(),name='generate-report'),
    path('analytics/',RecruiterAnalyticsAPIView.as_view(),name='analytics'),
    path('security-test/',SecurityTestAPIView.as_view()),
    path('security-report/',SecurityReportAPIView.as_view(),name='security-report'),
    path("subscription/access/",SubscriptionAccessAPIView.as_view()),
    path("payments/create-order/",CreatePaymentOrderAPIView.as_view(),name="create-payment-order"),
    path("payments/verify/",VerifyPaymentAPIView.as_view(),name="verify-payment"),
    path("payment-test/",PaymentTestView.as_view(),name="payment-test",),
    path("payments/webhook/",PaymentWebhookAPIView.as_view(),name="payment-webhook"),
    path("payments/history/",PaymentHistoryAPIView.as_view(),name="payment-history"),
    path("payments/<int:payment_id>/",PaymentDetailAPIView.as_view(),name="payment-detail"),
    path("payments/refund/",RefundPaymentAPIView.as_view(),name="payment-refund"),
    path("subscription/access/",SubscriptionAccessAPIView.as_view(),name="subscription-access"),
    path("premium/candidate-ranking/",CandidateRankingAPIView.as_view(),name="candidate-ranking"),
    path("premium/hiring-efficiency/",HiringEfficiencyAPIView.as_view(),name="hiring-efficiency"),
    path("premium/candidate-predictions/",CandidatePredictionAPIView.as_view(),name="candidate-predictions"),
    path("premium/dashboard/",PremiumDashboardAPIView.as_view(),name="premium-dashboard"),
    
    path("admin/finance/dashboard/",FinanceDashboardAPIView.as_view(),name="finance-dashboard"),

    path("admin/finance/daily-revenue/",DailyRevenueAPIView.as_view(),name="daily-revenue"),

    path("admin/finance/monthly-revenue/",MonthlyRevenueAPIView.as_view(),name="monthly-revenue"),

    path("admin/finance/plan-revenue/",PlanRevenueAPIView.as_view(),name="plan-revenue"),

    path("admin/finance/payment-failures/",PaymentFailureAPIView.as_view(),name="payment-failures"),
]