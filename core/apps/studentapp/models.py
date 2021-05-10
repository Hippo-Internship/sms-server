# Django built-in imports
from django.db import models
from django.contrib.auth import get_user_model
# Third party imports
# Local imports
from core import base_models
from core.apps.classapp import models as classapp_models

# User model
User = get_user_model()

class ClassStudent(base_models.BaseWithDate):

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='students', 
        null=False, 
        blank=False,
        db_index=True
    )
    operator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="registered_students",
        null=False,
        blank=False,
        db_index=True
    )
    _class = models.ForeignKey(
        classapp_models.Class, 
        on_delete = models.CASCADE,
        related_name='students', 
        null=False, 
        blank=False,
        db_column="class",
        db_index=True
    )
    # status = models.
    # payment_payed = models.IntegerField(null=True, default=0) # tulsun tulbur
    # total_payment = models.FloatField(null=True, default=0) # niit tulbur
    # payment_remain = models.FloatField(null=True, default=0) # vldsen tulber
    # discount_amount = models.IntegerField(default=0, null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
    note = models.CharField(max_length = 255, null=True, blank=True)
    canceled = models.BooleanField(null=False, default=False)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%d %d %d" % (self.id, self.user, self.operator)
    
