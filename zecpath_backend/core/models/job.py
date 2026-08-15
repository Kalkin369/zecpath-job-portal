from django.db import models

from .employer import Employer


class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    skills = models.TextField()

    experience = models.IntegerField(default=0)
    qualification = models.CharField(max_length=100)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)

    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        return self.title
