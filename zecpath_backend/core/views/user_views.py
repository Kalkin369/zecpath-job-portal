from rest_framework import viewsets
from core.models.user import User
from core.serializers.user__serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer