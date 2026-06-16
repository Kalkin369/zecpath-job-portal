from rest_framework import serializers

from core.models import (
    InterviewSchedule
)


class InterviewScheduleSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = InterviewSchedule

        fields = '__all__'