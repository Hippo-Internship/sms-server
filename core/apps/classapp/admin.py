# Django built-in imports
from django.contrib import admin
# Local imports
from . import models

# Register your models here.
admin.site.register(models.Room)
admin.site.register(models.Lesson)
admin.site.register(models.Class)
admin.site.register(models.Calendar)