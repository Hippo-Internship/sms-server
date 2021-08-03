from uuid import uuid4
import os
# Django built-in imports
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
# Local imports
from . import models as local_models
from core import functions as core_functions


@receiver(post_delete, sender=local_models.Curriculum)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)

@receiver(pre_save, sender=local_models.Curriculum)
def auto_delete_curriculum_on_change(sender, instance, **kwargs):
    try:
        curriculum = local_models.Curriculum.objects.get(id=instance.pk)
    except local_models.Curriculum.DoesNotExist:
        curriculum = None
    core_functions.handle_file_upload(instance, curriculum, "file", "curriculum")