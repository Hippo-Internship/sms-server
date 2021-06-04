# Django built-in imports
from django.db import models
from django.contrib.auth import get_user_model
# Local imports
from core import base_models
from core.apps.classapp import models as classapp_models
from core.apps.schoolapp import models as schoolapp_models

# User model
User = get_user_model()


class Status(models.Model):

    id = models.BigAutoField(primary_key=True)
    branch = models.ForeignKey(
        schoolapp_models.Branch,
        on_delete=models.CASCADE,
        related_name="datasheet_statuses",
        null=False,
        blank=False,
        db_index=True
    )
    name = models.CharField(max_length=36, null=False, blank=False)
    priority = models.IntegerField(null=False, default=0)

    def __str__(self):
        return "%s %s" % (self.id, self.name)
    


class Datasheet(base_models.BaseWithDate):

    REGISTER_TYPES = (
        ("Phone", "Phone"),
        ("Person", "In Person"),
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
        ("Website", "Website")
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,
        related_name="datasheets",
        null=False, 
        blank=False,
        db_index=True
    )
    operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="registered_datasheets", 
        null=True,
        blank=False,
        db_index=True
    )
    status = models.ForeignKey(
        Status, 
        on_delete=models.SET_NULL,
        related_name="datasheets", 
        null=True, 
        blank=True
    )
    lesson = models.ForeignKey(
        classapp_models.Lesson,
        on_delete=models.SET_NULL, 
        related_name="datasheets",
        null=True, 
        blank=True
    )
    branch = models.ForeignKey(
        schoolapp_models.Branch,
        on_delete=models.CASCADE,
        related_name="datasheets",
        null=False,
        blank=False,
        db_index=True
    )
    register_type = models.CharField(max_length=24, choices=REGISTER_TYPES, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    time = models.TimeField(null=False, blank=False, auto_now_add=True)

    class Meta: 
        ordering  = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.user, self.operator)
    