# Django imports
from django.contrib.auth import get_user_model
# Third Party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
# Local imports
from . import models as local_models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Profile
        fields = "__all__"
        extra_kwargs = {
            "user": { "required": False, "write_only": True }
        }


class CustomUserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'firstname',
            'lastname',
            'email',
            'phone',
            'password',
            'related_phone',
            'school',
            'branch',
            "profile",
            "groups"
        ]
        extra_kwargs = {
            "password": { "write_only": True },
            "school": { "required": True },
            "branch": { "required": True },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
        

class CustomUserUpdateSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
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
        read_only_fields = [ "school", "branch" ]