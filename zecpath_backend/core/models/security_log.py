from django.db import models


class SecurityLog(models.Model):

    ip_address = models.CharField(
        max_length=100
    )

    event = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )