from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

from core.models import UserSubscription

from core.permissions import IsAdmin, IsEmployer

from core.serializers.user_subscription_serializer import (
    UserSubscriptionSerializer
)

from core.views.base_viewset import BaseViewSet

from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema(
    tags=["User Subscriptions"]
)
@extend_schema_view(

    list=extend_schema(
        summary="Get User Subscriptions",
        description="Retrieve all user subscriptions. Admin only.",
        responses={
            200: UserSubscriptionSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Get User Subscription Detail",
        description="Retrieve a user subscription by ID.",
        responses={
            200: UserSubscriptionSerializer,
            404: OpenApiResponse(
                description="Subscription not found."
            ),
        },
    ),

    create=extend_schema(
        summary="Create User Subscription",
        description="Create a new user subscription. Admin only.",
        request=UserSubscriptionSerializer,
        responses={
            201: UserSubscriptionSerializer,
            400: OpenApiResponse(
                description="Validation error."
            ),
        },
    ),

    update=extend_schema(
        summary="Update User Subscription",
        description="Update an existing user subscription.",
        request=UserSubscriptionSerializer,
        responses={
            200: UserSubscriptionSerializer,
        },
    ),

    partial_update=extend_schema(
        summary="Partially Update User Subscription",
        description="Update selected fields of a user subscription.",
        request=UserSubscriptionSerializer,
        responses={
            200: UserSubscriptionSerializer,
        },
    ),

    destroy=extend_schema(
        summary="Delete User Subscription",
        description="Delete a user subscription.",
        responses={
            204: OpenApiResponse(
                description="User subscription deleted successfully."
            ),
        },
    ),

)
class UserSubscriptionViewSet(BaseViewSet):

    queryset = (
        UserSubscription.objects.select_related(
            "employer",
            "plan"
        )
    )

    serializer_class = (
        UserSubscriptionSerializer
    )

    permission_classes = [
        IsAdmin
    ]

    def get_permissions(self):

        if self.action == "my_subscription":
            permission_classes = [IsEmployer]
        else:
            permission_classes = [IsAdmin]

        return [
            permission()
            for permission in permission_classes
        ]

    @extend_schema(
        summary="My Active Subscription",
        description="Retrieve the authenticated employer's active subscription.",
        responses={
            200: UserSubscriptionSerializer,
            404: OpenApiResponse(
                description="No active subscription found."
            ),
        },
    )
    @action(detail=False, methods=["get"])
    def my_subscription(self, request):

        subscription = (
            UserSubscription.objects
            .select_related(
                "plan",
                "employer"
            )
            .filter(
                employer=request.user.employer,
                is_active=True
            )
            .first()
        )

        if not subscription:
            return Response(
                {
                    "message": "No active subscription found."
                },
                status=404
            )

        serializer = self.get_serializer(
            subscription
        )

        return Response(
            serializer.data
        )