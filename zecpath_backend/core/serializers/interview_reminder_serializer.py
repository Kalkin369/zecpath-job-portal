from rest_framework import serializers

from core.models import (InterviewReminder)


class InterviewReminderSerializer(serializers.ModelSerializer):

    class Meta:

        model = InterviewReminder

        fields = '__all__'