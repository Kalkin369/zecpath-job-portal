from django.db import models
from django.conf import settings

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return  self.company_name or self.user.email 