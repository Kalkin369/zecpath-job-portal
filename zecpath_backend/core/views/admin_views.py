from core.views.base_viewset import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdmin

from core.models.employer import Employer
from core.models.user import User
from core.models.job import Job
from core.models.application import Application

from core.serializers.employer_serializer import EmployerSerializer
from core.serializers.user_serializer import UserSerializer
from core.serializers.job_serializer import JobSerializer
from django.core.cache import cache




# Admin Employer APIs
class AdminEmployerViewSet(BaseViewSet):

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAdmin]

# Approve Employer Action
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):

        employer = self.get_object()

        employer.is_verified = True
        employer.save(update_fields=["is_verified"])

        return Response({
            "message": "Employer approved"
        })
    
# Admin User APIs
class AdminUserViewSet(BaseViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

#Block Action
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):

        user = self.get_object()

        user.is_blocked = True
        user.save(update_fields=["is_blocked"])

        return Response({
            "message": "User blocked"
        }) 
    
    
# Admin Job APIs
class AdminJobViewSet(BaseViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]    


#Spam Removal Action
    @action(detail=True, methods=['post'])
    def remove_spam(self, request, pk=None):

        job = self.get_object()

        job.status = 'inactive'
        job.save(update_fields=["status"])

        return Response({
            "message": "Spam job removed"
        }) 
    


# Dashboard Stats Action
    @action(detail=False, methods=['get'])
    def stats(self, request):

        cached_stats = cache.get('platform_stats')

        if cached_stats:
            return Response(cached_stats)

        data = {
            "total_users": User.objects.count(),
            "total_jobs": Job.objects.count(),
            "total_applications": Application.objects.count(),
            "total_employers": Employer.objects.count(),
        }

        cache.set('platform_stats',data,timeout=120)

        return Response(data)
       