from rest_framework import serializers
from core.models.ai_call import AICall

class AICallSerializer(serializers.ModelSerializer):

    class Meta:
        model = AICall
        fields ='__all__'