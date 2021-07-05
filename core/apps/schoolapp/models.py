# Django built-in imports
from django.db import models
# Local imports
from core import \
        base_models, \
        functions as core_functions

path_and_rename_school = core_functions.PathAndRename("image/schools")
path_and_rename_school_logo = core_functions.PathAndRename("image/schools-logo", "logo")
path_and_rename_branch = core_functions.PathAndRename("image/branches")

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
    color = models.CharField(max_length = 52, null=False, blank=True, default="#3d3f56")
    image = models.ImageField(upload_to="images/schools", null=False, blank=True, default="image/schools/default-min.jpg")
    logo = models.ImageField(upload_to="images/schools-logo", null=True, blank=True)

    class Meta: 
        ordering = [ "-id" ]

    def save(self, *args, **kwargs):
        if self.image:
            self.image = core_functions.compress_image(self.image)
        if self.logo:
            self.logo = core_functions.compress_image(self.logo)
        super(School, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.id, self.name)


class Branch(base_models.BaseWithDate):
    
    id = models.BigAutoField(primary_key=True)
    school = models.ForeignKey(
        School, 
        related_name="branches", 
        on_delete = models.CASCADE, 
        null=False,
        blank=False,
        db_index=True
    )
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
    image = models.ImageField(upload_to="images/branches", null=False, blank=True, default="image/branches/default_min.jpg")

    class Meta: 
        ordering = [ "-id" ]

    def save(self, *args, **kwargs):
        if self.image == None:
            super(Branch, self).save(*args, **kwargs)
            return
        self.image = core_functions.compress_image(self.image)
        super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s %s' % (self.id, self.name, self.school)