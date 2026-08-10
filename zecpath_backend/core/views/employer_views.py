from core.views.base_viewset import BaseViewSet
from core.models.employer import Employer
from core.serializers.employer_serializer import EmployerSerializer
from core.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


@extend_schema(
    tags=["Employers"]
)
@extend_schema_view(
    list=extend_schema(
        summary="List Employers",
        description="Retrieve the authenticated employer profile.",
        responses={
            200: EmployerSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Employer",
        description="Retrieve an employer profile.",
        responses={
            200: EmployerSerializer,
            404: OpenApiResponse(description="Employer not found"),
        },
    ),

    create=extend_schema(
        summary="Create Employer Profile",
        description="Create an employer profile for the authenticated user.",
        request=EmployerSerializer,
        responses={
            201: EmployerSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),

    update=extend_schema(
        summary="Update Employer Profile",
        description="Update an employer profile.",
        request=EmployerSerializer,
        responses={
            200: EmployerSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially Update Employer Profile",
        description="Update selected employer profile fields.",
        request=EmployerSerializer,
        responses={
            200: EmployerSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete Employer Profile",
        description="Delete an employer profile.",
        responses={
            204: OpenApiResponse(description="Employer deleted"),
        },
    ),
)


class EmployerViewSet(BaseViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsEmployer]
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['company_name']
    ordering_fields = ['id','user_email']


    def get_queryset(self):
        return (Employer.objects.select_related("user").filter(user=self.request.user))
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
