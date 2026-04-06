from django.db import models
from .candidate import Candidate
from .job import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied','Applied'),
        ('shortlisted','Shortlisted'),
        ('rejected','Rejected'),
    )    

    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='applied')   
    ats_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate} - {self.job}"