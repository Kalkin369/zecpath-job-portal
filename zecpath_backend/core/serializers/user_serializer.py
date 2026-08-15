from rest_framework import serializers

from core.models.user import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "role", "phone"]

    def create(self, validated_data):
        self.password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(self.password)
        user.save()
        return user
