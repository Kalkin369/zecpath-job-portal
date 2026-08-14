from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models.user import User
from core.serializers.user_serializer import UserSerializer

from django.contrib.auth import authenticate
from core.services.auth_service import generate_tokens
from core.utils.response import success_response
from rest_framework_simplejwt.tokens import RefreshToken
from core.services.logging_service import LoggingService
from core.utils.error_handler import handle_exception


from core.throttles import LoginThrottle

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

@extend_schema(
    tags=["Authentication"],
    summary="User Registration",
    description=(
        "Register a new user account. "
        "Supported roles are Candidate and Employer."
    ),
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            description="User created successfully."
        ),
        400: OpenApiResponse(
            description="Validation failed."
        ),
    },
    examples=[
        OpenApiExample(
            "Candidate Signup",
            value={
                "email": "candidate@example.com",
                "password": "Password@123",
                "role": "candidate",
                "phone": "9876543210"
            },
            request_only=True,
        ),
        OpenApiExample(
            "Employer Signup",
            value={
                "email": "employer@example.com",
                "password": "Password@123",
                "role": "employer",
                "phone": "9876543210"
            },
            request_only=True,
        ),
    ],
)

class SignupAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(
    tags=["Authentication"],
    summary="User Login",
    description=(
        "Authenticate a registered user and return "
        "JWT access and refresh tokens."
    ),
    request={
        "application/json": {
            "example": {
                "email": "candidate@example.com",
                "password": "Password@123"
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description="Login successful."
        ),
        401: OpenApiResponse(
            description="Invalid credentials."
        ),
        403: OpenApiResponse(
            description="Account blocked or not verified."
        ),
    },
)

class LoginAPI(APIView):

    throttle_classes = [LoginThrottle]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=401
            )

        if user.is_blocked:
            return Response(
                {"error": "Your account has been blocked."},
                status=403
            )

        if not user.is_staff and not user.is_verified:
            return Response(
                {"error": "Please verify your account first."},
                status=403
            )

        tokens = generate_tokens(user)

        return success_response(
            tokens,
            "Login successful"
        )
    
@extend_schema(
    tags=["Authentication"],
    summary="Refresh Access Token",
    description=(
        "Generate a new JWT access token using "
        "a valid refresh token."
    ),
    request={
        "application/json": {
            "example": {
                "refresh": "your_refresh_token"
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description="Access token refreshed."
        ),
        400: OpenApiResponse(
            description="Invalid or expired refresh token."
        ),
    },
)

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

            return success_response(
                {
                    "access":access_token
                },
                "Token refreshed"
            )

        except Exception as e:

            return handle_exception(
                "RefreshAPI",e,"Invalid or expired refresh token",status.HTTP_400_BAD_REQUEST
            )