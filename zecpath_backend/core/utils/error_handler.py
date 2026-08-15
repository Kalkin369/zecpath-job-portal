from rest_framework.response import Response

from core.services.logging_service import LoggingService


def handle_exception(view_name, error, message="Operation failed", status_code=500):

    LoggingService().create_error_log(view_name, str(error))

    return Response({"error": message}, status=status_code)
