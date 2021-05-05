# Django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractUser
# Local imports
from . import validators as local_validators

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

    ROLES = (
        (1, "SuperAdmin"),
        (2, "Admin"),
        (3, "Operator"),
        (4, "Teacher"),
        (5, "Student"),
        (6, "Accountant"),
        (7, "Staff"),
    )

    first_name = models.CharField(null=True, blank=False, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    username = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(unique=True, null=True, db_index=True)
    phone = models.CharField(validators=[ local_validators.validate_phone ], max_length=20, null=False)
    related_phone = models.CharField(validators = [ local_validators.validate_phone ], max_length=20, null=True, blank=True)
    role_id = models.IntegerField(null=False, choices=ROLES, blank=False)
    interested_at = models.CharField(null=True, max_length=255)
    school_id = models.IntegerField(null=True, default=0)
    branch_id = models.IntegerField(null=True, default=0)
    seen_datasheet = models.IntegerField(null=True, default=3)
    is_active = models.IntegerField(null=True, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'role_id']

    objects = CustomUserManager()

    @property
    def role_name(self):
        return self.ROLES[self.role_id - 1][1]

    def __str__(self):
        return '%s: %s: %s' % (self.phone, self.first_name, self.last_name)

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='image', blank=True, default="")
    address_city = models.CharField(null=True, blank=True, max_length=255, default="")
    address_district = models.CharField(null=True, blank=True, max_length=255, default="")
    address_khoroo = models.CharField(blank=True, max_length=255, default="")
    address_appartment = models.CharField(blank=True, max_length=255, default="")
    dob = models.CharField(blank=True, max_length=255, default="")
    register = models.CharField(max_length=255, blank=True, default="")

    @property
    def image_url(self):
        return '{}{}'.format(settings.MEDIA_URL, self.profile_image)

    def __str__(self):
        return str(user)