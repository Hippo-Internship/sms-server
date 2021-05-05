# Django built-in imports
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
# Local imports
# from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def test(sender, instance, created, **kwargs): 
    # if created:
    #     Profile.objects.create(user_id=instance)
    print(instance)