from django.db import models
from django.conf import settings

class NotificationLog(models.Model):

    STATUS_CHOICES = (
        ('success','Success'),
        ('failed','Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    subject = models.CharField(max_length=225)

    message = models.TextField()

    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

    error_message =models.TextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
