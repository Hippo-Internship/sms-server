# Django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group
# Local imports
from . import validators as local_validators
from core.apps.schoolapp import models as schoolapp_models

# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("role_id", 1)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be a staff!")
        
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be a superuser :)!")
        
        return self.create_user(email, password, **kwargs)


class CustomUser(AbstractUser):

    SUPER_ADMIN = 1
    ADMIN = 2
    OPERATOR = 3
    TEACHER = 4
    STUDENT = 5
    ACCOUNTANT = 6
    STAFF = 7

    ROLES = (
        (SUPER_ADMIN, "SuperAdmin"),
        (ADMIN, "Admin"),
        (OPERATOR, "Operator"),
        (TEACHER, "Teacher"),
        (STUDENT, "Student"),
        (ACCOUNTANT, "Accountant"),
        (STAFF, "Staff"),
    )

    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(null=True, blank=True, max_length=100)
    lastname = models.CharField(null=True, blank=True, max_length=100)
    username = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(
        unique=True, null=False, db_index=True,
        error_messages={
            "unique": "This email is already registered!"
        }
    )
    phone = models.CharField(
        validators=[ local_validators.validate_phone ], 
        max_length=20, null=False, unique=True, 
        error_messages={
            "unique": "This number is already registered!"
        }
    )
    related_phone = models.CharField(validators = [ local_validators.validate_phone ], max_length=20, null=True, blank=True)
    interested_at = models.CharField(null=True, max_length=255, blank=True)
    school = models.ForeignKey(schoolapp_models.School, on_delete=models.CASCADE, null=True, blank=True, related_name="users")
    branch = models.ForeignKey(schoolapp_models.Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="users")
    seen_datasheet = models.IntegerField(null=True, default=3)
    is_active = models.IntegerField(null=True, default=1)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="users")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'role_id']

    objects = CustomUserManager()

    class Meta:
        ordering = [ 'id' ]

    @property
    def role_name(self):
        return self.ROLES[self.role_id - 1][1]

    def __str__(self):
        return '%s %s %s: %s' % (self.id, self.phone, self.first_name, self.last_name)


class Profile(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(upload_to='image/profiles', null=True, blank=True)
    address_city = models.CharField(null=True, blank=True, max_length=255)
    address_district = models.CharField(null=True, blank=True, max_length=255)
    address_khoroo = models.CharField(null=True, blank=True, max_length=255)
    address_appartment = models.CharField(null=True, blank=True, max_length=255)
    dob = models.DateField(null=True, blank=True, max_length=255)
    register = models.CharField(null=True, max_length=255, blank=True)

    def __str__(self):
        return '%s %s' % (self.id, self.user)