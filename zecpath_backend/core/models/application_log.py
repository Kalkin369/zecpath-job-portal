from django.db import models
from core.models.application import Application

class ApplicationLog(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - {self.old_status} → {self.new_status}"