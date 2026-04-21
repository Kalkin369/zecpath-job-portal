from rest_framework import viewsets
from core.models.user import User
from core.serializers.user__serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated, IsAdmin]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['email']
    ordering_fields = ['id','email']