# Django built-in imports
from django.db import models
# Local imports
from core import base_models
from core.apps.schoolapp import models as schoolapp_models

class Status(base_models.BaseWithDate):

    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(
        schoolapp_models.Branch,
        on_delete=models.CASCADE,
        related_name="status",
        null=True,
        blank=True,
        db_index=True
    )
    name = models.CharField(max_length=26, null=False, blank=False)
    color = models.CharField(max_length=7, null=False, default="#3d3f56")
    default = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = [ "-default", "-id" ]
        unique_together = [ "branch", "name" ]

    def __str__(self):
        return "%s %s" % (self.id, self.branch)
    

class PaymentMethod(base_models.BaseWithDate):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=26, null=False, blank=False)
    branch = models.ForeignKey(
        schoolapp_models.Branch,
        on_delete=models.CASCADE,
        related_name="payment_method",
        null=True,
        blank=True,
        db_index=True
    )
    default = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = [ "-default", "-id" ]
        unique_together = [ "branch", "name" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.branch)
    
