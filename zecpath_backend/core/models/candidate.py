from django.db import models
from django.conf import settings

class Candidate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email