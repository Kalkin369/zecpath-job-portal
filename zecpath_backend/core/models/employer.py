from django.db import models
from .user import User

class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return  self.company_name   