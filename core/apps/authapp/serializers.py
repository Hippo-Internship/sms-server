# Django imports
from django.contrib.auth import get_user_model
# Third Party imports
from rest_framework import serializers
# Local imports
from . import models as local_models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Profile
        fields = "__all__"
        extra_kwargs = {
            "user": { "write_only": True }
        }


class CustomUserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password',
            'related_phone',
            'school_id',
            'branch_id',
            "profile",
            "groups"
        ]
        extra_kwargs = {
            "password": { "write_only": True }
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
            'first_name',
            'last_name',
            'email',
            'phone',
            'related_phone',
            'school_id',
            'branch_id',
            "profile",
            "groups"
        ]
        read_only_field = [ "school_id", "branch_id" ]