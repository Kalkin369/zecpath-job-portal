from rest_framework.views import APIView
from rest_framework.response import Response

from core.services.logging_service import (LoggingService)
from core.permissions import IsAdmin

from core.models import (SecurityLog)
from core.serializers.security_log_serializer import (SecurityLogSerializer)
from drf_spectacular.utils import extend_schema,OpenApiResponse,OpenApiExample

@extend_schema(
    tags=["Security"],
    summary="Generate Security Test Log",
    description=(
        "Generate a sample security event for testing the security logging system."
    ),
    responses={
        200: OpenApiResponse(
            description="Security log created successfully."
        ),
    },
    examples=[
        OpenApiExample(
            "Success",
            value={
                "message": "Security Log Created"
            },
            response_only=True,
        )
    ],
)




class SecurityTestAPIView(APIView):

    def get(self,request):

        LoggingService().create_security_log(
            request.META.get(
                'REMOTE_ADDR',
                'Unknown'
            ),
            "Unauthorized Access Attempt"
        )

        return Response(
            {
                "message":
                "Security Log Created"
            }
        )
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

@extend_schema(
    tags=["Security Logs"]
)

@extend_schema_view(

    list=extend_schema(
        summary="List Security Logs",
        description="Retrieve all recorded security events.",
        responses={
            200: SecurityLogSerializer(many=True),
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Security Log",
        description="Retrieve a security log by ID.",
        responses={
            200: SecurityLogSerializer,
            404: OpenApiResponse(
                description="Security log not found."
            ),
        },
    ),

    
)
    
class SecurityLogViewSet(

    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,

):

    queryset = (SecurityLog.objects.all().order_by('-created_at'))

    serializer_class = (SecurityLogSerializer)

    permission_classes = [IsAdmin]    