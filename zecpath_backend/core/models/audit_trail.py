from django.db import models

from .user import User

class AuditTrail(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    action = models.CharField(max_length=255)

    entity_type = models.CharField(max_length=100)

    entity_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user} - " f"{self.action}"
