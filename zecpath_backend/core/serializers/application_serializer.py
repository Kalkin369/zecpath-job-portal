from rest_framework import serializers
from core.models.application import Application


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source='candidate.user.full_name',
        read_only=True
    )
    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'resume',
            'status',
            'applied_at',
            'candidate_name',
            'job_title'
        ]
        read_only_fields = ['status', 'applied_at']