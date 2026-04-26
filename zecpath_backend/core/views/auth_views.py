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
from core.services.auth_service import generate_tokens
from core.utils.response import success_response


class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        tokens = generate_tokens(user)

        return success_response(tokens, "Login successful")
    

from rest_framework_simplejwt.tokens import RefreshToken


class RefreshAPI(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({
                "status": "fail",
                "message": "Refresh token required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Token refreshed",
                "data": {
                    "access": access_token
                }
            })

        except Exception:
            return Response({
                "status": "fail",
                "message": "Invalid or expired refresh token"
            }, status=status.HTTP_400_BAD_REQUEST)    