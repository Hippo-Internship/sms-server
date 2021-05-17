# Third party imports
from rest_framework import serializers
# Local imports
from . import models as local_models


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Status
        fields = "__all__"


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.PaymentMethod
        fields = "__all__"