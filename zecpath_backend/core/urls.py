from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *
from core.views.auth_views import SignupAPI,LoginAPI,RefreshAPI
from core.views.saved_job_views import SavedJobViewSet



router = DefaultRouter()
router.register('users', UserViewSet)
router.register('employers', EmployerViewSet,basename='employer')
router.register('candidates', CandidateViewSet,basename='candidate')
router.register('jobs', JobViewSet)
router.register('applications', ApplicationViewSet)
router.register('saved-jobs',SavedJobViewSet,basename='saved-jobs')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    path('auth/refresh/',RefreshAPI.as_view()),
]