# Third party imports
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
# Local imports
from . import models as local_models


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"
        extra_kwargs = {
            "default": { "read_only": True },
            "branch": { "required": True },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['branch', 'name'],
                message="Name is already registered!"
            )
        ]

class StatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"
        extra_kwargs = {
            "branch": { "required": False },
            "default": { "read_only": True }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['branch', 'name'],
                message="Name is already registered!"
            )
        ]

    def validate_branch(self, value):
        if value.id != self.instance.branch.id:
            return serializers.ValidationError("Branch can't be changed!")
        return value

class ShortStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = [ "id", "name", "default" ]

class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = "__all__"
        extra_kwargs = {
            "default": { "read_only": True },
            "branch": { "required": True },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['branch', 'name'],
                message="Name is already registered!"
            )
        ]

class PaymentMethodWithAnnotation(serializers.ModelSerializer):

    total = serializers.FloatField(read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = local_models.PaymentMethod
        exclude = [ "created", "modified" ]
        extra_kwargs = {
            "default": { "read_only": True }
        }

class StatusWithAnnotation(serializers.ModelSerializer):

    count = serializers.IntegerField(read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = local_models.Status
        exclude = [ "created", "modified" ]


class ShortPaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = [ "id", "name", "default" ]
        
class PaymentMethodUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = "__all__"
        extra_kwargs = {
            "branch": { "required": False },
            "default": { "read_only": True }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['branch', 'name'],
                message="Name is already registered!"
            )
        ]

    def validate_branch(self, value):
        if value.id != self.instance.branch.id:
            return serializers.ValidationError("Branch can't be changed!")
        return value