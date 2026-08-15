from rest_framework import serializers

from core.models.call_log import CallLog


class CallLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallLog
        fields = "__all__"
