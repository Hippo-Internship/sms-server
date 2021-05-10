# Django built-in imports
from django.db import models
from django.contrib.auth import get_user_model
# Local imports
from core.apps.schoolapp import models as schoolapp_models
from core import base_models

# User model
User = get_user_model()

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
        max_length=50, unique=True, null=False, blank=False, db_index=True,
        error_messages={
            "unique": "Name is already regeistered!"
        }
    )
    short_name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    interval = models.PositiveIntegerField(null=True, default=0)
    is_online_pay = models.BooleanField(null=True, blank=True)
    sort = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=False, blank=False)
    color = models.CharField(max_length=50, default="#3d3f56")
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
        max_length=50, unique=True, null=False, blank=False, db_index=True,
        error_messages={
            "unique": "Name is already registered!"
        }
    )
    capacity = models.PositiveIntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.branch)
    

class Class(models.Model):

    id = models.BigAutoField(primary_key=True)
    branch = models.ForeignKey(
        schoolapp_models.Branch,
        related_name='classes', 
        on_delete = models.CASCADE, 
        null=False,
        blank=False,
        db_index=True
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name='classes', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )
    teacher = models.ForeignKey(
        User, 
        related_name='classes', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_index=True
    )
    room = models.ForeignKey(
        Room, 
        related_name='classes', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        db_index=True
    )
    name = models.CharField(max_length=56, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    note = models.CharField(max_length=255, null=True, blank=True)
    interval = models.PositiveIntegerField(null = True, blank = True)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.branch, self.lesson)


class Calendar(models.Model):

    DAYS = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )

    id = models.AutoField(primary_key=True)
    _class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="dates",
        null=False,
        blank=False,
        db_column="class",
        db_index=True
    )
    day = models.IntegerField(choices=DAYS)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.day)
    