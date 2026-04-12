from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *
from core.views.auth_views import SignupAPI,LoginAPI



router = DefaultRouter()
router.register('users', UserViewSet)
router.register('employers', EmployerViewSet,basename='employer')
router.register('candidates', CandidateViewSet,basename='candidate')
router.register('jobs', JobViewSet)
router.register('applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignupAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
]