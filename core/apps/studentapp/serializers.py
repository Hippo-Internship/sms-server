# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
# Local imports
from . import models as local_models

# User model
User = get_user_model()

class StudentCreateOrModifySerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Student
        fields = "__all__"
        extra_kwargs = {
            "_class": { "required": False },
            "operator": { "required": False }
        }

    def validate(self, data):
        _class = data["_class"]
        if _class.branch.id is not data["user"].branch.id:
            raise PermissionDenied()
        if _class.branch.id is not data["status"].branch.id:
            raise PermissionDenied()
        return data

    def validate_user(self, value):
        if value.groups.role_id is not User.STUDENT:
            raise ValidationError("User should be student!")
        return value
        