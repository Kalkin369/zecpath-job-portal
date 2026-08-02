from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # optional

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate','Candidate'),
        ('employer','Employer'),
        ('admin','Admin')
    )

    username = None
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,db_index=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email