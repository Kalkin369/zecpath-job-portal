from django.db import models
from django.conf import settings
from ..validators import validate_resume


def resume_upload_path(instance,filename):
    return f"resumes/user_{instance.user.id}/{filename}"

class Candidate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    skills = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    expected_salary = models.IntegerField(null=True,blank=True)
    resume = models.FileField(upload_to=resume_upload_path,validators=[validate_resume],null=True,blank=True)

    def __str__(self):
        return self.user.email