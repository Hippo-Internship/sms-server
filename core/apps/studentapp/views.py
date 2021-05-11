# Django built-in imports
from django.shortcuts import render
from django.db.models import Sum
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

    queryset = local_models.Student.objects.all()
    serializer_class = local_serializers.StudentCreateOrModifySerializer

    def list(self, request):
        # students = self.get_queryset().annotate(total_paid=Sum("payments__paid"))
        # print(students[0].total_paid)
        students = local_models.User.objects.filter(groups__role_id=local_models.User.STUDENT)
        students = local_serializers.UserStudentsDetailSerializer(students, many=True)
        return core_responses.request_success_with_data(students.data)
        # request_user = request.user
        # filter_params = local_utils.normalize_data(
        #     { 
        #         "teacher": "int",
        #         "lesson": "int",
        #     },
        #     dict(request.query_params)
        # )
        # if request_user.groups.role_id == User.SUPER_ADMIN:
        #     classes = self.get_queryset().all()
        # elif request_user.groups.role_id == User.ADMIN:
        #     branches = request_user.school.branches.all()
        #     classes = self.get_queryset().filter(branch__in=branches, **filter_params)
        # elif request_user.groups.role_id == User.OPERATOR:
        #     classes = self.get_queryset().filter(branch=request_user.branch, **filter_params)
        # elif request_user.groups.role_id == User.TEACHER:
        #     classes = self.get_queryset().filter(teacher=request_user, **filter_params)
        # p_classes = self.paginate_queryset(classes)
        # classes = self.get_serializer_class()(p_classes, many=True)
        # return self.get_paginated_response(classes.data)


