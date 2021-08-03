from uuid import uuid4
import os
# Django built-in imports
from django.db.models.signals import post_save, post_delete, pre_save
from django.conf import settings
from django.dispatch import receiver
# Local imports
from . import models as local_models
from core import functions as core_functions
from django.core.files.storage import default_storage

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        local_models.Profile.objects.create(user=instance)

@receiver(post_delete, sender=local_models.Profile)
def auto_delete_profile_on_delete(sender, instance, **kwargs):
    if instance.image:
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)

@receiver(pre_save, sender=local_models.Profile)
def auto_delete_profile_on_change(sender, instance, **kwargs):
    try:
        profile = local_models.Profile.objects.get(id=instance.pk)
    except local_models.Profile.DoesNotExist:
        profile = None
    return core_functions.handle_file_upload(instance, profile, "image", "images/profiles")
