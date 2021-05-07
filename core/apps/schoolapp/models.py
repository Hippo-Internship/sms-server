# Django built-in imports
from django.db import models
# Local imports
from core import base_models


class School(base_models.BaseWithDate):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=36, unique=True, null=False, blank=False,
        error_messages={
            "unique": "Name is already registered!"
        }
    )
    description = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    website = models.CharField(max_length=52, null=True, blank=True)
    color = models.CharField(max_length = 52, null=False, default="#3d3f56")
    image = models.ImageField(upload_to = "image/schools", blank=True, null=True)
    logo = models.ImageField(upload_to = "image/schools-logo", blank=True, null=True)

    class Meta: 
        ordering = [ "id" ]

    def __str__(self):
        return '%s %s' % (self.id, self.name)


class Branch(base_models.BaseWithDate):
    
    id = models.BigAutoField(primary_key=True)
    school = models.ForeignKey(
        School, 
        related_name="branches", 
        on_delete = models.CASCADE, 
        db_index=True)
    name = models.CharField(
        max_length=36, unique=True, null=False, blank=False,
        error_messages={
            "unique": "Name is already registered!"
        }
    )
    description = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    website = models.CharField(max_length=52, null=True, blank=True)
    image = models.ImageField(upload_to = "image/branches", blank=True, null=True)

    class Meta: 
        ordering = [ "id" ]

    def __str__(self):
        return '%s %s %s' % (self.id, self.name, self.school)
    
    
# class PaymentMethod(models.Model):
    
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length = 100)
#     branches = models.ManyToManyField(Branch, related_name="payment_methods")

#     class Meta:
#         ordering = [ "id" ]

#     def __str__(self):
#         return "%s %s" % (self.id, self.name)
    

# class Status(models.Model):

#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=24, null=False, blank=False)
#     color = models.CharField(max_length=24, null=False, default="#3d3f56")
#     branches = models.ManyToManyField(Branch, related_name="statuses")

#     class Meta:
#         ordering = [ "id" ]

#     def __str__(self):
#         return "%s %s" % (self.id, self.name)
    