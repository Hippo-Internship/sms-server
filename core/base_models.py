# Django built-in imports
from django.db import models

class BaseWithDate(models.Model):

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True
