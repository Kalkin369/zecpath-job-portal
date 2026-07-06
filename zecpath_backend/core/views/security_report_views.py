from rest_framework.views import APIView

from rest_framework.response import Response

from core.permissions import IsAdmin


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