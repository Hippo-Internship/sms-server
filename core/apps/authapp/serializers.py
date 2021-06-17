# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Third Party imports
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError, PermissionDenied
# Local imports
from . import models as local_models

# User model
User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Profile
        fields = "__all__"
        extra_kwargs = {
            "user": { "required": False, "write_only": True }
        }


class CustomUserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(CustomUserSerializer, self).__init__(*args, **kwargs)

    profile = UserProfileSerializer(read_only=True)
    role_id = serializers.IntegerField(source="groups.role_id", read_only=True)
    role_name = serializers.CharField(source="groups.name", read_only=True)
    school_name = serializers.CharField(source="school.name", read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    job_hour = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'firstname',
            'lastname',
            'email',
            'phone',
            'password',
            'related_phone',
            'school',
            "school_name",
            "branch_name",
            'branch',
            "profile",
            "groups",
            "role_id",
            "role_name",
            "job_hour"
        ]
        extra_kwargs = {
            "password": { "write_only": True },
            "school": { "required": True },
            "branch": { "required": False },
        }

    def validate(self, data):
        if data["groups"].role_id <= User.ADMIN:
            data.pop("branch", None)
        return data

    def validate_groups(self, value):
        if value.role_id <= self.user.groups.role_id:
            raise PermissionDenied()
        return value

    def create(self, validated_data):
        if "password" not in validated_data:
            return super().create(validated_data)
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
        

class CustomUserUpdateSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(CustomUserUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            'id',
            'firstname',
            'lastname',
            'email',
            'phone',
            'related_phone',
            'school',
            'branch',
            "profile",
            "groups"
        ]
        read_only_fields = [ "school", "branch", "groups" ]
        extra_kwargs = {
            "firstname": { "required": False },
            "phone": { "required": False },
        }

class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [ "id", "firstname", "lastname", "phone" ]


class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [ "id", "name", "role_id" ]