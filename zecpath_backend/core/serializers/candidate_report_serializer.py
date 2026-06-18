from rest_framework import serializers

from core.models import (
    CandidateReport
)


class CandidateReportSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = CandidateReport

        fields = '__all__'