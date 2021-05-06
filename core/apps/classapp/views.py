# Django built-in imports
from django.shortcuts import render
# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
# Local imports
from . import models as local_models
from . import serializers as local_serializers


class LessonViewSet(viewsets.ModelViewSet):

    queryset = local_models.Lesson.objects.all()
    serializer_class = local_serializers.LessonSerializer


