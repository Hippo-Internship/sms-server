from uuid import uuid4
import os
# Django built-in imports
from django.db.models.signals import post_save, post_delete, pre_save
from django.conf import settings
from django.dispatch import receiver
# Local imports
from . import models as local_models
from core import functions as core_functions

@receiver(post_delete, sender=local_models.School)
@receiver(post_delete, sender=local_models.Branch)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=local_models.School)
def auto_delete_school_on_change(sender, instance, **kwargs):
    try:
        school = local_models.School.objects.get(id=instance.pk)
    except local_models.School.DoesNotExist:
        return False
    core_functions.handle_image_upload(instance, school, "image")
    core_functions.handle_image_upload(instance, school, "logo")

@receiver(pre_save, sender=local_models.Branch)
def auto_delete_branch_on_change(sender, instance, **kwargs):
    try:
        branch = local_models.Branch.objects.get(id=instance.pk)
    except local_models.School.DoesNotExist:
        return False
    core_functions.handle_image_upload(instance, branch, "image")