# Python imports
from datetime import date
# Django built-in imports
from django.contrib.auth import get_user_model
from django.db.models import Sum, fields
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
# Local imports
from . import models as local_models
from core.apps.authapp import serializers as authapp_serializers

# User model
User = get_user_model()

class StudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Student
        fields = "__all__"
        extra_kwargs = {
            "_class": { "required": False },
            "operator": { "required": False }
        }

    def validate(self, data):
        _class = data["_class"]
        if (_class.branch.id is not data["user"].branch.id or 
            _class.branch.id is not data["status"].branch.id or
            "payment_paid" in data or "discount_amount" in data):
            raise PermissionDenied()
        if "discounts" in data:
            for discount in data["discounts"]:
                if _class.branch.id is not discount.branch.id:
                    raise PermissionDenied()
                if discount.limited and discount.limit == discount.count:
                    raise serializers.ValidationError("Invalid discount!")
                if discount.end_date < date.today():
                    raise serializers.ValidationError("Invalid discount!")
        return data

    def validate_user(self, value):
        if value.groups.role_id is not User.STUDENT:
            raise serializers.ValidationError("User should be student!")
        return value


class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Student
        exclude = [ "user", "operator"]
        extra_kwargs = {
            "_class": { "required": False }
        }

    def validate(self, data):
        _class = self.instance._class
        print(self.instance.status)
        print(data)
        if (_class.branch.id is not data["status"].branch.id or
            "payment_paid" in data or "discount_amount" in data):
            raise PermissionDenied()
        if "discounts" in data:
            for discount in data["discounts"]:
                if _class.branch.id is not discount.branch.id:
                    raise PermissionDenied()
                if discount.limited and discount.limit == discount.count:
                    raise serializers.ValidationError("Invalid discount!")
                if discount.end_date < date.today():
                    raise serializers.ValidationError("Invalid discount!")
        return data


class DiscountDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Discount
        fields = "__all__"


class DiscountShortDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Discount
        fields = [ "id", "name" ]


class ExamResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.ExamResult
        exclude = [ "created", "modified" ]
        extra_kwargs = {
            "student": { "write_only": True }
        }

    def validate(self, data):
        exam = data["exam"]
        student = data["student"]
        if exam._class.id != student._class.id:
            raise PermissionDenied()
        return data


class JournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Journal
        fields = "__all__"
        extra_kwargs = {
            "student": { "write_only": True },
        }


class StudentShortDetailSerializer(serializers.ModelSerializer):

    discounts = DiscountShortDetailSerializer(many=True)
    user_firstname = serializers.CharField(source="user.firstname")
    user_lastname = serializers.CharField(source="user.lastname")
    status_name = serializers.CharField(source="status.name")
    total_payment = serializers.FloatField(source="_class.lesson.price")
    exam_results = ExamResultSerializer(many=True, read_only=True)
    journals = JournalSerializer(many=True, read_only=True)

    class Meta:
        model = local_models.Student
        exclude = [ 
            "_class", 
            "created", 
            "modified",
            "start_date",
            "end_date"
        ]


class StudentFullDetailSerializer(serializers.ModelSerializer):

    students = StudentShortDetailSerializer(many=True, read_only=True)
    profile = authapp_serializers.UserProfileSerializer(read_only=True)

    class Meta:
        model = local_models.User
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
            "groups",
            "students",
        ]


class UserStudentsDetailSerializer(serializers.ModelSerializer):

    students = StudentShortDetailSerializer(many=True, read_only=True)
    groups = serializers.IntegerField(source="groups.role_id", read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'firstname',
            'lastname',
            'email',
            'school',
            'branch',
            "groups",
            "students"
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Payment
        fields = "__all__"

    
class PaymentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Payment
        fields = "__all__"
        read_only_fields = [ "id", "student" ]



class ShortDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Discount
        fields = [ "id", "name" ]


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Note
        fields = "__all__"


class NoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Note
        fields = "__all__"
        read_only_fields = [ "id", "student" ]
