# Django built-in imports
from django.db import models
# Local imports
from core.apps.schoolapp import models as schoolapp_models
from core import base_models

# Create your models here.
class Lesson(base_models.BaseWithDate):

    id = models.BigAutoField(primary_key=True)
    branch = models.ForeignKey(
        schoolapp_models.Branch, 
        on_delete=models.CASCADE, 
        null=False, 
        related_name="lessons", 
        db_index=True
    )
    name = models.CharField(
        max_length=50, unique=True, null=False, blank=False,
        error_messages={
            "unique": "Name is already regeistered!"
        }
    )
    short_name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=255, null = True, blank=True)
    interval = models.PositiveIntegerField(null=True, default=0)
    is_online_pay = models.BooleanField(null = True, blank=True)
    sort = models.PositiveIntegerField(null = True, blank=True)
    price = models.PositiveIntegerField(null = False, blank=False)
    color = models.CharField(max_length = 50, default="#3d3f56")
    sort = models.PositiveIntegerField(null=True, blank=True)
    exam = models.PositiveIntegerField(null=True, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.branch)
    


class Room(base_models.BaseWithDate):

    id = models.BigAutoField(primary_key=True)
    branch = models.ForeignKey(
        schoolapp_models.Branch, 
        on_delete=models.CASCADE, 
        null=False, 
        related_name="rooms", 
        db_index=True
    )
    name = models.CharField(
        max_length=50, unique=True, null=False, blank=False,
        error_messages={
            "unique": "Name is already registered!"
        }
    )
    capacity = models.PositiveIntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.branch)
    