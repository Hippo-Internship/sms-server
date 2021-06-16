# Django imports
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group
# Local imports
from . import validators as local_validators
from core import functions as core_functions
from core.apps.schoolapp import models as schoolapp_models

# Adding custom field to the group
Group.add_to_class('role_id', models.IntegerField(null=False, blank=False, default=7))

path_and_rename = core_functions.PathAndRename("image/profiles")

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
        kwargs.setdefault("groups", Group.objects.get(id=1))
        kwargs.setdefault("phone", "99999999")

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

    FORBIDDEN_FILTER = {
        SUPER_ADMIN: [],
        ADMIN: [ "school" ],
        OPERATOR: [ "school", "branch" ],
        TEACHER: [ "school", "branch" ],
        STUDENT: [ "school", "branch" ],
        ACCOUNTANT: [ "school", "branch" ],
        STAFF: [ "school", "branch" ],
    }

    CREATED_FROM_DATASHEET = 1
    DATASHEET_AND_STUDENT = 2
    CREATED_FROM_STUDENT = 3

    SEEN_DATASHEET_TYPE = (
        (CREATED_FROM_DATASHEET, "Created from datasheet"),
        (DATASHEET_AND_STUDENT, "Student and registered in datasheet"),
        (CREATED_FROM_STUDENT, "Created from student")
    )

    id = models.BigAutoField(primary_key=True)
    school = models.ForeignKey(
        schoolapp_models.School, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="users", 
        db_index=True
    )
    branch = models.ForeignKey(
        schoolapp_models.Branch, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="users", 
        db_index=True)
    firstname = models.CharField(max_length=56, null=False, blank=False)
    lastname = models.CharField(max_length=56, null=True, blank=True)
    username = models.CharField(max_length=56, null=True, blank=True)
    email = models.EmailField( 
        unique=True, null=True, blank=True,
        error_messages={
            "unique": "This email is already registered!"
        }
    )
    password = models.CharField(_('password'), max_length=128, null=True, blank=True)
    phone = models.CharField(
        validators=[ local_validators.validate_phone ], 
        max_length=20, null=False, unique=True, 
        error_messages={
            "unique": "This number is already registered!"
        }
    )
    related_phone = models.CharField(validators = [ local_validators.validate_phone ], max_length=20, null=True, blank=True)
    interested_at = models.CharField(null=True, max_length=255, blank=True)
    seen_datasheet = models.IntegerField(null=False, blank=True, choices=SEEN_DATASHEET_TYPE, default=SEEN_DATASHEET_TYPE[2][0])
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="users")
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = [ "-id" ]

    @property
    def students_count(self):
        if self.groups.role_id != self.STUDENT:
            return 0
        return len(self.students.filter(canceled=False))

    @students_count.setter
    def students_count(self, value):
        print(value)

    def __str__(self):
        return '%s %s %s: %s' % (self.id, self.phone, self.first_name, self.last_name)


class Profile(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='profile',
        db_index=True
    )
    image = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    address_city = models.CharField(null=True, blank=True, max_length=255)
    address_district = models.CharField(null=True, blank=True, max_length=255)
    address_khoroo = models.CharField(null=True, blank=True, max_length=255)
    address_appartment = models.CharField(null=True, blank=True, max_length=255)
    dob = models.DateField(null=True, blank=True, max_length=255)
    register = models.CharField(null=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.image  or self.image == None:
            super(Profile, self).save(*args, **kwargs)
            return
        self.image = core_functions.compress_image(self.image)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.id, self.user)