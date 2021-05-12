# Django built-in imports
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
# Local imports
from . import models as local_models

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        local_models.Profile.objects.create(user=instance)