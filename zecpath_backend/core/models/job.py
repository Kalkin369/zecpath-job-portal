from django.db import models
from .employer import Employer

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.CharField(max_length=200)
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,null=True,blank=True)
    experience_required = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
