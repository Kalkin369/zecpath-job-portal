from django.db import models
from core.models.candidate import Candidate
from core.models.job import Job

class SavedJob(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate','job')

    def __str__(self):
        return f"{self.candidate} saved {self.job}"    