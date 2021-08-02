# Django built-in imports
# Third party imports
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# Local imports
from . import models as local_models


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.School
        fields = "__all__"

        
class BranchSerializer(serializers.ModelSerializer):

    school_name = serializers.CharField(source="school.name", read_only=True)
    school_image = serializers.ImageField(source="school.image", read_only=True)

    class Meta:
        model = local_models.Branch
        fields = "__all__"


class BranchUpdateSerializer(serializers.ModelSerializer):

    school_name = serializers.CharField(source="school.name", read_only=True)
    school_image = serializers.ImageField(source="school.image", read_only=True)

    class Meta:
        model = local_models.Branch
        fields = "__all__"
        extra_kwargs = {
            "school": { "read_only": True }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['school', 'name'],
                message="Name is already registered!"
            )
        ]


class SchoolShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.School
        fields = [ "id", "name" ]


class BranchShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Branch
        fields = [ "id", "name" ]


class BranchWithAnnotationSerializer(serializers.ModelSerializer):

    total = serializers.FloatField(read_only=True)

    class Meta:
        model = local_models.Branch
        fields = [ "id", "name", "total", "image", "website" ]