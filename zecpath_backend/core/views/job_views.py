from core.views.base_viewset import BaseViewSet
from core.models.job import Job
from core.serializers.job_serializer import JobSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from core.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache


class JobViewSet(BaseViewSet):
    queryset = Job.objects.select_related('employer')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['experience','job_type','location']
    search_fields = ['title','skills','location']
    ordering_fields = ['created_at','experience','salary_min']

    def get_permissions(self):
        if self.action in ['list','retrieve','latest','featured']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated(),IsEmployer()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
      queryset = Job.objects.select_related('employer')

    # 🔹 Query params (filters)
      min_salary = self.request.query_params.get('min_salary')
      max_salary = self.request.query_params.get('max_salary')

      if min_salary:
        queryset = queryset.filter(salary_min__gte=min_salary)

      if max_salary:
        queryset = queryset.filter(salary_max__lte=max_salary)

      user = self.request.user

    # 🔹 Employer → see own jobs
      if user.is_authenticated and hasattr(user, 'employer'):
         return queryset.filter(employer=user.employer)

    # 🔹 Public/Candidate → only active jobs
      return queryset.filter(status='active')
    
    def perform_create(self, serializer):
     user = self.request.user

     if not hasattr(user, 'employer'):
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Only employers can create jobs")

     serializer.save(employer=user.employer)
   
# Toggle status  
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        job = self.get_object()

        # Check ownership
        if not hasattr(request.user, 'employer') or job.employer != request.user.employer:
            return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        # Toggle status
        job.status = 'inactive' if job.status == 'active' else 'active'
        job.save()

        return Response({"message": "Job status updated"})
    
#Latest Jobs 
    @action(detail=False,methods=['get'])
    def latest(self,request):
       
       cached_jobs = cache.get('latest_jobs')

       if cached_jobs:
          return Response (cached_jobs)
       
       jobs = self.queryset.filter(status='active').order_by('created_at')[:10]
       serializer = self.get_serializer(jobs, many=True)

       cache.set('latest_jobs',serializer.data,timeout=60)
       
       return Response(serializer.data)
    
#Featured Jobs
    @action(detail=False, methods=['get'])
    def featured(self,request):
       
       cached_jobs = cache.get('featured_jobs')

       if cached_jobs:
          return Response(cached_jobs)
       

       jobs = self.queryset.filter(status='active',experience__lte=2)[:5]
       serializer = self.get_serializer(jobs, many=True)

       cache.set('featured_jobs',serializer.data,timeout=60)

       return Response(serializer.data)
      
#Profile based Recommendations
    @action(detail=False, methods=['get'])
    def recommended(self, request):

        user = request.user

        if not hasattr(user, 'candidate'):
            return Response({"error": "Only candidates allowed"}, status=403)

        candidate = user.candidate

        skills = candidate.skills.split(',')

        queryset = Job.objects.filter(status='active')

        matched_jobs = []

        for job in queryset:
            job_skills = job.skills.lower()

            for skill in skills:
                if skill.strip().lower() in job_skills:
                    matched_jobs.append(job)
                    break

        serializer = self.get_serializer(matched_jobs, many=True)

        return Response(serializer.data)  