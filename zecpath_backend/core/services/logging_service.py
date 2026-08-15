from core.models import AuditTrail, ErrorLog, SecurityLog


class LoggingService:

    def create_audit_log(self, user, action, entity_type, entity_id):

        AuditTrail.objects.create(
            user=user, action=action, entity_type=entity_type, entity_id=entity_id
        )

    def create_error_log(self, source, message):

        ErrorLog.objects.create(source=source, message=message)

    def create_security_log(self, ip_address, event):

        SecurityLog.objects.create(ip_address=ip_address, event=event)
