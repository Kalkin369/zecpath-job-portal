from django.db import models


class QuestionTemplate(models.Model):

    CATEGORY_CHOICES = [
        ("introduction", "Introduction"),
        ("experience", "Experience"),
        ("skills", "Skills"),
        ("availability", "Availability"),
        ("salary", "Salary"),
    ]

    role = models.CharField(max_length=100)

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    question = models.TextField()

    expected_keywords = models.JSONField(default=list, blank=True)

    weight = models.FloatField(default=1)

    is_follow_up = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
