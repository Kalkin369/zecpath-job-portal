from django.db import models

# Create your models here.

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
    
class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return  self.company_name   
    
class Candidate(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name
    
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.CharField(max_length=200)
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,null=True,blank=True)
    experience_required = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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