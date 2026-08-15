from rest_framework import serializers

from core.models.notification_log import NotificationLog


class NotificationLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationLog
        fields = "__all__"
