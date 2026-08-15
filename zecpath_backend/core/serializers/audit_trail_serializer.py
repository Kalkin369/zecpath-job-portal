from rest_framework import serializers

from core.models import AuditTrail


class AuditTrailSerializer(serializers.ModelSerializer):

    class Meta:

        model = AuditTrail

        fields = "__all__"
