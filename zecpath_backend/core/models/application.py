from django.db import models

from core.utils.file_upload import resume_upload_path

from ..validators import validate_resume
from .candidate import Candidate
from .job import Job


class Application(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview Sheduled"),
        ("rejected", "Rejected"),
        ("selected", "Selected"),
    )

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, db_index=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, db_index=True)
    resume = models.FileField(
        upload_to=resume_upload_path,
        validators=[validate_resume],
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="applied", db_index=True
    )
    ats_score = models.FloatField(default=0)
    applied_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ["candidate", "job"]

    def __str__(self):
        return f"{self.candidate} - {self.job}"
