# Django built-in imports
from django.contrib import admin
# Local improts
from . import models

# Register your models here.
admin.site.register(models.Status)
admin.site.register(models.PaymentMethod)