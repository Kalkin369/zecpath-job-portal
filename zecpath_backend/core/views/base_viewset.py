from rest_framework.viewsets import ModelViewSet

from core.services.logging_service import LoggingService
from core.utils.response import success_response


class BaseViewSet(ModelViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(response.data)

    def create(self, request, *args, **kwargs):

        response = super().create(request, *args, **kwargs)

        LoggingService().create_audit_log(
            request.user,
            "CREATE",
            self.get_queryset().model.__name__,
            response.data.get("id"),
        )

        return success_response(
            response.data, message="Created Successfully", status_code=201
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        LoggingService().create_audit_log(
            request.user, "UPDATE", self.get_queryset().model.__name__, kwargs.get("pk")
        )
        return success_response(response.data, message="Updated successfully")

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        LoggingService().create_audit_log(
            request.user,
            "PARTIAL_UPDATE",
            self.get_queryset().model.__name__,
            kwargs.get("pk"),
        )

        return success_response(response.data, message="Updated successfully")

    def destroy(self, request, *args, **kwargs):
        object_id = kwargs.get("pk")

        LoggingService().create_audit_log(
            request.user, "DELETE", self.get_queryset().model.__name__, object_id
        )

        super().destroy(request, *args, **kwargs)

        return success_response(message="Deleted successfully")
