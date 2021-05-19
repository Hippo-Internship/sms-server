# Django built-in imports
from re import T
from django.db import models
from django.contrib.auth import get_user_model
# Third party imports
# Local imports
from core import base_models
from core.apps.classapp import models as classapp_models
from core.apps.utilityapp import models as utilityapp_models
from core.apps.schoolapp import models as schoolapp_models

# User model
User = get_user_model()

class Discount(models.Model):

    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(
        schoolapp_models.Branch,
        on_delete=models.CASCADE,
        related_name="discounts",
        null=False,
        blank=False,
        db_index=True
    )
    name = models.CharField(max_length=56, null=False, blank=True, unique=True)
    percent = models.FloatField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    limited = models.BooleanField(null=True, default=False)
    limit = models.IntegerField(null=False, blank=True, default=0)
    count = models.IntegerField(null=False, blank=True, default=0)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s" % (self.id, self.name)

class Student(base_models.BaseWithDate):

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
    status = models.ForeignKey(
        utilityapp_models.Status, 
        on_delete=models.CASCADE,
        related_name="students",
        null=False,
        blank=False,
        db_index=True
    )
    payment_paid = models.IntegerField(null=False, default=0)
    discount_amount = models.FloatField(null=False, default=0)
    discounts = models.ManyToManyField(Discount, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    note = models.CharField(max_length = 255, null=True, blank=True)
    canceled = models.BooleanField(null=False, default=False)

    class Meta:
        ordering = [ "id" ]
        unique_together = [ "user", "_class" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.user, self.operator)
    

class Payment(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(
        Student, 
        on_delete = models.CASCADE,
        related_name="payments",
        null=False,
        blank=False,
        db_index=True
    )
    pay_type = models.ForeignKey(
        utilityapp_models.PaymentMethod,
        on_delete = models.CASCADE, 
        related_name="payments", 
        null=False,
        blank=False, 
        db_index=True
    )
    paid = models.FloatField(null=False, blank=False)
    is_debit = models.BooleanField(null=False, default=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = [ "id" ]

    def __str__(self):
        return "%s %s" % (self.id, self.student)
    

class Note(base_models.BaseWithDate):

    id = models.AutoField(primary_key=True)
    operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="student_notes",
        null=True,
        blank=False,
        db_index=True
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="notes",
        null=False,
        blank=False,
        db_index=True
    )
    body = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return "%s %s" % (self.id, self.student)


class Journal(models.Model):

    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name="journals",
        null=False,
        blank=False,
        db_index=True
    )
    date = models.DateField(null=False, blank=False)
    state = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return "%s %s" % (self.id, self.student)


class ExamResult(base_models.BaseWithDate):

    id = models.BigAutoField(primary_key=True)
    exam = models.ForeignKey(
        classapp_models.Exam,
        on_delete=models.CASCADE,
        related_name="results",
        null=False,
        blank=False,
        db_index=True
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="exam_results",
        null=False,
        blank=False,
        db_index=True
    )
    mark = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = [ "id" ]
        unique_together = [ "exam", "student" ]

    def __str__(self):
        return "%s %s %s" % (self.id, self.student, self.exam)