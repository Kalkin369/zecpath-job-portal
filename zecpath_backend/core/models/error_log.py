from django.db import models


class ErrorLog(models.Model):

    source = models.CharField(max_length=100)

    message = models.TextField()

    stack_trace = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
