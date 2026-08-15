from rest_framework import serializers

from core.models.job import Job


class JobSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(
        source="employer.company_name", read_only=True
    )

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["employer", "status"]
