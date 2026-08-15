from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema
    )
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema(
    tags=["Authentication"],
    summary="Logout User",
    description=(
        "Blacklist the provided refresh token " "to securely log the user out."
    ),
    request={"application/json": {"example": {"refresh": "your_refresh_token"}}},
    responses={
        200: OpenApiResponse(description="Logout successful."),
        400: OpenApiResponse(description="Invalid refresh token."),
    },
)
class LogoutAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh = request.data.get("refresh")

        if not refresh:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            token = RefreshToken(refresh)

            token.blacklist()

            return Response({"message": "Logout successful."})

        except Exception:

            return Response(
                {"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST
            )
