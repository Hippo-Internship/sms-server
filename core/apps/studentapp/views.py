# Django built-in imports
from django.shortcuts import render
# Third Party imports
from rest_framework import viewsets
from rest_framework.response import Response
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers
from core import \
        decorators as core_decorators, \
        permissions as core_permissions, \
        responses as core_responses

class StudentViewSet(viewsets.GenericViewSet):

    queryset = local_models.Student
    serializer_class = local_serializers.StudentCreateOrModifySerializer

    def create(self, request):
        student_request_data = request.data
        student = self.get_serializer_class()(data=student_request_data)
        student.is_valid(raise_exception=True)
        return core_responses.request_success()

