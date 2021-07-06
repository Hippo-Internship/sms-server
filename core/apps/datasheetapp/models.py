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
        null=True,
        blank=True,
        db_index=True
    )
    name = models.CharField(max_length=26, null=False, blank=False)
    priority = models.IntegerField(null=False, default=0)
    default = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        unique_together = [ "branch", "name" ]
        ordering = [ "-default" ]

    def __str__(self):
        return "%s %s" % (self.id, self.name)
    


class Datasheet(base_models.BaseWithDate):

    OTHER = 0
    PHONE = 1
    IN_PERSON = 2
    FACEBOOK = 3
    INSTAGRAM = 4
    WEBSITE = 5

    REGISTER_TYPES = (
        (OTHER, "Other"),
        (PHONE, "Phone"),
        (IN_PERSON, "In Person"),
        (FACEBOOK, "Facebook"),
        (INSTAGRAM, "Instagram"),
        (WEBSITE, "Website")
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
    register_type = models.IntegerField(choices=REGISTER_TYPES, null=False, blank=False, default=OTHER)
    description = models.CharField(max_length=255, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta: 
        ordering  = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.user, self.operator)
    