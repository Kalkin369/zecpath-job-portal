from rest_framework import serializers
from core.models.saved_job import SavedJob


class SavedJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ['candidate']