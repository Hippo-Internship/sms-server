# Python imports
from datetime import date
# Django built-in imports
from django.contrib.auth import get_user_model
from django.db.models import Sum
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
        for discount in data["discounts"]:
            if _class.branch.id is not discount.branch.id:
                raise PermissionDenied()
            if discount.end_date < date.today():
                raise serializers.ValidationError("Invalid discount!")
        return data

    def validate_user(self, value):
        if value.groups.role_id is not User.STUDENT:
            raise serializers.ValidationError("User should be student!")
        return value


class StudentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Student
        fields = "__all__"

    def to_representation(self, instance):
        return super(StudentDetailSerializer, self).to_representation(instance)


class UserStudentsDetailSerializer(serializers.ModelSerializer):

    students = StudentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        return super(UserStudentsDetailSerializer, self).to_representation(instance)