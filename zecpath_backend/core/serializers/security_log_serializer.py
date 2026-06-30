from rest_framework import serializers

from core.models import (
    SecurityLog
)


class SecurityLogSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = SecurityLog

        fields = '__all__'