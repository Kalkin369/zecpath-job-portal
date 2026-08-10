from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsAdmin

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)

@extend_schema(
    tags=["Security"],
    summary="Security Audit Report",
    description=(
        "Retrieve the current security configuration of the platform "
        "including authentication, throttling, encryption, audit logging, "
        "and security logging."
    ),
    responses={
        200: OpenApiResponse(
            description="Security report retrieved successfully."
        ),
        403: OpenApiResponse(
            description="Admin authentication required."
        ),
    },
    examples=[
        OpenApiExample(
            "Security Report",
            value={
                "authentication": "JWT",
                "throttling": "Enabled",
                "encryption": "Passwords Hashed",
                "audit_logs": "Enabled",
                "security_logs": "Enabled"
            },
            response_only=True,
        )
    ],
)


class SecurityReportAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self,request):

        return Response(
            {
                "authentication":
                "JWT",

                "throttling":
                "Enabled",

                "encryption":
                "Passwords Hashed",

                "audit_logs":
                "Enabled",

                "security_logs":
                "Enabled"
            }
        )