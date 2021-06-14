# Third party imports
from django.db.models import fields
from rest_framework import serializers
# Local imports
from . import models as local_models


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"


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