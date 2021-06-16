# Third party imports
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
# Local imports
from . import models as local_models


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"

class StatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"
        extra_kwargs = {
            "branch": { "required": False }
        }

    def validate_branch(self, value):
        if value.id != self.instance.branch.id:
            return serializers.ValidationError("Branch can't be changed!")
        return value

class ShortStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = [ "id", "name" ]

class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = "__all__"

class ShortPaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = [ "id", "name" ]
        
class PaymentMethodUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = "__all__"
        extra_kwargs = {
            "branch": { "required": False }
        }

    def validate_branch(self, value):
        if value.id != self.instance.branch.id:
            return serializers.ValidationError("Branch can't be changed!")
        return value