# Python imports
from datetime import date
# Django built-in imports
from django.contrib.auth import get_user_model
from django.db.models import Sum
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueTogetherValidator
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
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['_class', 'user'],
                message="User is already registered in the class!"
            )
        ]

    def validate(self, data):
        _class = data["_class"]
        if (_class.branch.id is not data["user"].branch.id or 
            (not data["status"].default and _class.branch.id is not data["status"].branch.id) or
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
        if not data["status"].default and _class.branch.id != data["status"].branch.id:
            raise PermissionDenied()
        if "payment_paid" in data:
            data.pop("payment_paid")
        if "discount_amount" in data:
            data.pop("discount_amount")
        if "discounts" in data:
            for discount in data["discounts"]:
                if _class.branch.id != discount.branch.id:
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

class DiscountUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Discount
        fields = "__all__"
        extra_kwargs = {
            "branch": { "required": False }
        }

    def validate(self, data):
        if "percent" in data:
            data["value"] = None
        elif "value" in data:
            data["percent"] = None
        elif "percent" not in data and "value" not in data:
            raise serializers.ValidationError("Should give percent or value!")
        return data
        
    def validate_branch(self, value):
        if value.id != self.instance.branch.id:
            return serializers.ValidationError("Branch can't be changed!")
        return value


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

    def validate(self, data):
        student = data["student"]
        calendar = data["calendar"]
        if student._class.id != calendar._class.id:
            raise PermissionDenied()
        return data


class StudentShortDetailSerializer(serializers.ModelSerializer):

    discounts = DiscountShortDetailSerializer(many=True)
    user_firstname = serializers.CharField(source="user.firstname", read_only=True)
    user_lastname = serializers.CharField(source="user.lastname", read_only=True)
    status_name = serializers.CharField(source="status.name", read_only=True)
    total_payment = serializers.FloatField(source="_class.lesson.price", read_only=True)
    payments_paid = serializers.IntegerField(read_only=True)
    user_branch = serializers.IntegerField(source="user.branch.id", read_only=True)
    exam_results = ExamResultSerializer(many=True, read_only=True)
    journals = JournalSerializer(many=True, read_only=True)

    class Meta:
        model = local_models.Student
        exclude = [ 
            "_class", 
            "created", 
            "modified",
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

    students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'firstname',
            'lastname',
            "phone",
            'email',
            'school',
            'branch',
            "groups",
            "students_count"
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class_name = serializers.CharField(source="student._class.name", read_only=True)

    class Meta:
        model = local_models.Payment
        fields = "__all__"

    def validate(self, data):
        student = data["student"]
        total_payment = student.payments.aggregate(total=Sum("paid"))
        remaining_fee = student._class.lesson.price - (total_payment["total"] if total_payment["total"] is not None else 0)
        if data["paid"] > remaining_fee:
            raise serializers.ValidationError("Value can't be more than remainder!")
        return data

    
class PaymentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Payment
        fields = "__all__"
        read_only_fields = [ "id", "student", "branch" ]



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


class StudentSubDetailSerializer(serializers.ModelSerializer):

    discounts = DiscountShortDetailSerializer(many=True)
    status_name = serializers.CharField(source="status.name", read_only=True)
    total_payment = serializers.FloatField(source="_class.lesson.price", read_only=True)
    payments_paid = serializers.IntegerField(read_only=True)
    class_name = serializers.CharField(source="_class.name", read_only=True)
    lesson_name = serializers.CharField(source="_class.leeson.name", read_only=True)
    class_id = serializers.IntegerField(source="_class.id", read_only=True)

    class Meta:
        model = local_models.Student
        exclude = [ 
            "_class", 
            "created", 
            "modified",
        ]