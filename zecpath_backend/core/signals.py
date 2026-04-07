from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.user import User
from core.models.candidate import Candidate
from core.models.employer import Employer


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'candidate':
            Candidate.objects.create(
                user=instance,
                phone="",  # default empty
                qualification="",
                experience=0
            )

        elif instance.role == 'employer':
            Employer.objects.create(
                user=instance,
                company_name=""  # default empty
            )