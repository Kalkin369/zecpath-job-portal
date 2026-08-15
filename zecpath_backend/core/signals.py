from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.candidate import Candidate
from core.models.employer import Employer
from core.models.user import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "candidate":
            Candidate.objects.create(
                user=instance, phone="", qualification="", experience=0  # default empty
            )

        elif instance.role == "employer":
            Employer.objects.create(user=instance, company_name="")  # default empty
