from core.models import SubscriptionPlan

from core.permissions import IsAdmin

from core.serializers.subscription_plan_serializer import (
    SubscriptionPlanSerializer
)

from core.views.base_viewset import BaseViewSet

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


@extend_schema(
    tags=["Subscription Plans"]
)
@extend_schema_view(
    list=extend_schema(
        summary="Get Subscription Plans",
        description="Retrieve all available subscription plans.",
        responses={200: SubscriptionPlanSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get Subscription Plan Detail",
        description="Retrieve a subscription plan by ID.",
        responses={
            200: SubscriptionPlanSerializer,
            404: OpenApiResponse(description="Subscription plan not found"),
        },
    ),
    create=extend_schema(
        summary="Create Subscription Plan",
        description="Create a new subscription plan. Admin only.",
        request=SubscriptionPlanSerializer,
        responses={
            201: SubscriptionPlanSerializer,
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    update=extend_schema(
        summary="Update Subscription Plan",
        description="Update an existing subscription plan.",
        request=SubscriptionPlanSerializer,
        responses={200: SubscriptionPlanSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update Subscription Plan",
        description="Update selected fields of a subscription plan.",
        request=SubscriptionPlanSerializer,
        responses={200: SubscriptionPlanSerializer},
    ),
    destroy=extend_schema(
        summary="Delete Subscription Plan",
        description="Delete a subscription plan.",
        responses={
            204: OpenApiResponse(description="Subscription plan deleted"),
        },
    ),
)


class SubscriptionPlanViewSet(BaseViewSet):

    queryset = (SubscriptionPlan.objects.all())

    serializer_class = (SubscriptionPlanSerializer)

    permission_classes = [IsAdmin]