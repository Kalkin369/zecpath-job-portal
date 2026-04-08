from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models.user import User
from core.serializers.user__serializer import UserSerializer


class SignupAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)

        return Response(serializer.errors, status=400)
    

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })    