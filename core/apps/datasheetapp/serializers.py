# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
# Local imports
from . import models as local_models


class DatasheetCreateSerializer(serializers.ModelSerializer):

    user_phone = serializers.CharField(source="user.phone", read_only=True)
    user_firstname = serializers.CharField(source="user.firstname", read_only=True)
    user_lastname = serializers.CharField(source="user.lastname", read_only=True)
    operator_firstname = serializers.CharField(source="operator.firstname", read_only=True)

    class Meta:
        model = local_models.Datasheet
        fields = "__all__"
        extra_kwargs = {
            "operator": { "required": True },
            "time": { "required": False },
            "user": { "required": False }
        }

    def validate(self, data):
        branch = data["branch"]
        operator = data["operator"]
        if operator.groups.role_id == local_models.User.OPERATOR and operator.branch.id != branch.id:
            raise PermissionDenied()
        if operator.groups.role_id == local_models.User.ADMIN and operator.branch.school.id != branch.school.id:
            raise PermissionDenied()
        if (("user" in data and data["user"] is not None and branch.id != data["user"].branch.id) or
            ("lesson" in data and data["lesson"] is not None and branch.id != data["lesson"].branch.id) or
            ("status" in data and data["status"] is not None and branch.id != data["status"].branch.id)):
            raise PermissionDenied()
        return data

    def validate_user(self, value):
        if value.is_active is False:
            raise serializers.ValidationError("Teacher does not exist!")
        return value

    def validate_operator(self, value):
        if value.groups.role_id not in [ local_models.User.OPERATOR, local_models.User.SUPER_ADMIN, local_models.User.ADMIN ]:
            raise PermissionDenied()
        if value.is_active is False:
            raise serializers.ValidationError("Teacher does not exist!")
        return value


class DatasheetUpdateSerializer(serializers.ModelSerializer):

    user_phone = serializers.CharField(source="user.phone", read_only=True)
    user_firstname = serializers.CharField(source="user.firstname", read_only=True)
    user_lasttname = serializers.CharField(source="user.lastname", read_only=True)
    operator_firstname = serializers.CharField(source="operator.firstname", read_only=True)

    class Meta:
        model = local_models.Datasheet
        exclude = [ "created", "modified" ]
        extra_kwargs = {
            "id": { "read_only": True },
            "user": { "read_only": True },
            "operator": { "read_only": True },
            "branch": { "read_only": True },
        }

    def validate(self, data):
        branch = self.instance.branch
        if (("lesson" in data and data["lesson"] is not None and branch.id != data["lesson"].branch.id) or
            ("status" in data and data["status"] is not None and branch.id != data["status"].branch.id)):
            raise PermissionDenied()
        return data


class DatasheetStatuSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"


class ShortDatasheetStatuSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = [ "id", "name", "branch" ]