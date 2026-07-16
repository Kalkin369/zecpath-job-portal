from rest_framework.serializers import ModelSerializer

from core.models import BillingHistory


class BillingHistorySerializer(ModelSerializer):

    class Meta:

        model = BillingHistory

        fields = "__all__"