from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    JobViewSet,
    ApplicationViewSet,
    EmployerViewSet,
    CandidateViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('employers', EmployerViewSet)
router.register('candidates', CandidateViewSet)
router.register('jobs', JobViewSet)
router.register('applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]