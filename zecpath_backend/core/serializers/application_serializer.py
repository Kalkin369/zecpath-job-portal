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
    job_company = serializers.CharField(
        source='job.employer.company_name',
        read_only=True
    )
    job_status = serializers.CharField(
        source='job.status',read_only=True
    )
    status_message = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id',
            'candidate',
            'job',
            'resume',
            'status',
            'ats_score',
            'applied_at',
            'candidate_name',
            'job_title',
            'job_company',
            'job_status',
            'status_message'
        ]
        read_only_fields = ['status', 'applied_at']

    def get_status_message(self,obj):
        return f"Your application is currently {obj.status}"    