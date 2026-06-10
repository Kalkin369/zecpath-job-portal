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
]