# Django built-in imports
from django.contrib import admin
# Local imports
from . import models

# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Payment)
admin.site.register(models.Discount)
admin.site.register(models.Note)