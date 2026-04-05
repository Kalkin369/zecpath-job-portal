from rest_framework import viewsets
from .models import User, Job, Application, Employer, Candidate
from .serializers import (
    UserSerializer,
    JobSerializer,
    ApplicationSerializer,
    EmployerSerializer,
    CandidateSerializer
)


#  User CRUD
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#  Employer CRUD
class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


#  Candidate CRUD
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


#  Job CRUD
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


#  Application CRUD
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer