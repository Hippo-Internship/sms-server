# Django built-in imports
# Third party imports
from rest_framework import serializers
# Local imports
from . import models as local_models


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.School
        fields = "__all__"

        
class BranchSerializer(serializers.ModelSerializer):

    school = serializers.CharField(source="school.name")

    class Meta:
        model = local_models.Branch
        fields = "__all__"