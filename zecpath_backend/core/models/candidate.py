from django.db import models
from .user import User

class Candidate(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name