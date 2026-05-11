from rest_framework import viewsets
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




# Admin Employer APIs
class AdminEmployerViewSet(viewsets.ModelViewSet):

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAdmin]

# Approve Employer Action
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):

        employer = self.get_object()

        employer.is_verified = True
        employer.save()

        return Response({
            "message": "Employer approved"
        })
    
# Admin User APIs
class AdminUserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

#Block Action
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):

        user = self.get_object()

        user.is_blocked = True
        user.save()

        return Response({
            "message": "User blocked"
        }) 
    
    
# Admin Job APIs
class AdminJobViewSet(viewsets.ModelViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]    


#Spam Removal Action
    @action(detail=True, methods=['post'])
    def remove_spam(self, request, pk=None):

        job = self.get_object()

        job.status = 'inactive'
        job.save()

        return Response({
            "message": "Spam job removed"
        }) 
    


# Dashboard Stats Action
    @action(detail=False, methods=['get'])
    def stats(self, request):

        data = {
            "total_users": User.objects.count(),
            "total_jobs": Job.objects.count(),
            "total_applications": Application.objects.count(),
            "total_employers": Employer.objects.count(),
        }

        return Response(data)
       