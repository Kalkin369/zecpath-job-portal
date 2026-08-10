from core.views.base_viewset import BaseViewSet
from core.models.user import User
from core.serializers.user_serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

@extend_schema(
    tags=["Users"]
)

@extend_schema_view(

    list=extend_schema(
        summary="List Users",
        description="Retrieve all registered users. Admin only.",
        responses={
            200: UserSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve User",
        description="Retrieve a user by ID.",
        responses={
            200: UserSerializer,
            404: OpenApiResponse(
                description="User not found."
            ),
        },
    ),

    create=extend_schema(
        summary="Create User",
        description=(
            "Create a new user manually. "
            "Normally users are created using the Signup API."
        ),
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(
                description="Validation error."
            ),
        },
    ),

    update=extend_schema(
        summary="Update User",
        description="Update an existing user.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially Update User",
        description="Update selected user fields.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete User",
        description="Delete a user.",
        responses={
            204: OpenApiResponse(
                description="User deleted successfully."
            ),
        },
    ),

)

class UserViewSet(BaseViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "email"
    ]

    ordering_fields = [
        "id",
        "email",
    ]