# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
# Local imports
from . import models as local_models


class DatasheetCreateSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    firstname = serializers.CharField(source="user.lastname", read_only=True)

    class Meta:
        model = local_models.Datasheet
        fields = "__all__"
        extra_kwargs = {
            "operator": { "required": True },
            "time": { "required": False }
        }

    def validate(self, data):
        branch = data["branch"]
        if (branch.id != data["user"].branch.id or
            ("lesson" in data and branch.id != data["lesson"].branch.id) or
            branch.id != data["operator"].branch.id or 
            ("status" in data and branch.id != data["status"].branch.id)):
            raise PermissionDenied()
        return data

    def validate_operator(self, value):
        if value.groups.role_id not in [ local_models.User.OPERATOR, local_models.User.SUPER_ADMIN, local_models.User.ADMIN ]:
            raise PermissionDenied()
        return value