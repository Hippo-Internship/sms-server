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
        (1, "Phone"),
        (2, "In Person"),
        (3, "Facebook"),
        (4, "Instagram"),
        (5, "Website")
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
    register_type = models.IntegerField(choices=REGISTER_TYPES, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta: 
        ordering  = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.user, self.operator)
    