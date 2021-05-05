# Django imports
from django.contrib.auth import get_user_model
# Third Party imports
from rest_framework import serializers
# Local imports
from . import models as local_models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Profile
        exclude = [ "user" ]

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
            'related_phone',
            'role_id',
            'school_id',
            'branch_id',
            "profile"
        ]