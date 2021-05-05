# Django built-in imports
from django.db import models
# Local imports
from core import base_models


class School(base_models.BaseWithDate):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=True)
    description = models.CharField(max_length=255)
    address = models.CharField(max_length = 255)
    website = models.CharField(max_length = 50)
    color = models.CharField(max_length = 50, default="green")
    school_image = models.ImageField(upload_to = 'image/schools', blank=True, null=True)
    logo = models.ImageField(upload_to = 'image', blank=True, null=True)

    class Meta: 
        ordering = [ "id" ]

    def __str__(self):
        return "{} {}".format(self.id, self.name)

