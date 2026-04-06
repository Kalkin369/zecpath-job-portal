from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ('candidate','Candidate'),
        ('employer','Employer'),
        ('admin','Admin')
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name