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

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

@extend_schema(
    tags=["Admin Management"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List Employers",
        description="Retrieve all employers.",
        responses={200: EmployerSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Employer Detail",
        description="Retrieve employer details.",
        responses={200: EmployerSerializer},
    ),
    create=extend_schema(
        summary="Create Employer",
        request=EmployerSerializer,
        responses={201: EmployerSerializer},
    ),
    update=extend_schema(
        summary="Update Employer",
        request=EmployerSerializer,
        responses={200: EmployerSerializer},
    ),
    partial_update=extend_schema(
        summary="Partial Update Employer",
        request=EmployerSerializer,
        responses={200: EmployerSerializer},
    ),
    destroy=extend_schema(
        summary="Delete Employer",
        responses={
            204: OpenApiResponse(
                description="Employer deleted"
            )
        },
    ),
)

# Admin Employer APIs
class AdminEmployerViewSet(BaseViewSet):

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAdmin]


    @extend_schema(
    summary="Approve Employer",
    description="Approve an employer account.",
    responses={
        200: OpenApiResponse(
            description="Employer approved"
        )
    }
    )

# Approve Employer Action
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):

        employer = self.get_object()

        employer.is_verified = True
        employer.save(update_fields=["is_verified"])

        return Response({
            "message": "Employer approved"
        })


@extend_schema(
    tags=["Admin Management"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List Users",
        responses={200: UserSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="User Detail",
        responses={200: UserSerializer},
    ),
    create=extend_schema(
        summary="Create User",
        request=UserSerializer,
        responses={201: UserSerializer},
    ),
    update=extend_schema(
        summary="Update User",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    partial_update=extend_schema(
        summary="Partial Update User",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    destroy=extend_schema(
        summary="Delete User",
        responses={
            204: OpenApiResponse(
                description="User deleted"
            )
        },
    ),
)
   
    
# Admin User APIs
class AdminUserViewSet(BaseViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @extend_schema(
    summary="Block User",
    description="Block a user account.",
    responses={
        200: OpenApiResponse(
            description="User blocked"
        )
    }
    )


#Block Action
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):

        user = self.get_object()

        user.is_blocked = True
        user.save(update_fields=["is_blocked"])

        return Response({
            "message": "User blocked"
        }) 
    
@extend_schema(
    tags=["Admin Management"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List Jobs",
        responses={200: JobSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Job Detail",
        responses={200: JobSerializer},
    ),
    create=extend_schema(
        summary="Create Job",
        request=JobSerializer,
        responses={201: JobSerializer},
    ),
    update=extend_schema(
        summary="Update Job",
        request=JobSerializer,
        responses={200: JobSerializer},
    ),
    partial_update=extend_schema(
        summary="Partial Update Job",
        request=JobSerializer,
        responses={200: JobSerializer},
    ),
    destroy=extend_schema(
        summary="Delete Job",
        responses={
            204: OpenApiResponse(
                description="Job deleted"
            )
        },
    ),
)


# Admin Job APIs
class AdminJobViewSet(BaseViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]    

    @extend_schema(
    summary="Remove Spam Job",
    description="Deactivate a spam or fraudulent job posting.",
    responses={
        200: OpenApiResponse(
            description="Spam job removed"
        )
    }
    )

    
#Spam Removal Action
    @action(detail=True, methods=['post'])
    def remove_spam(self, request, pk=None):

        job = self.get_object()

        job.status = 'inactive'
        job.save(update_fields=["status"])

        return Response({
            "message": "Spam job removed"
        }) 
    
    @extend_schema(
    summary="Platform Statistics",
    description="Retrieve platform-wide dashboard statistics.",
    responses={
        200: OpenApiResponse(
            description="Platform statistics"
        )
    }
    )


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
       