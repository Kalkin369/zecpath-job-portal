from rest_framework.serializers import ModelSerializer

from core.models import SubscriptionPlan


class SubscriptionPlanSerializer(ModelSerializer):

    class Meta:

        model = SubscriptionPlan

        fields = "__all__"