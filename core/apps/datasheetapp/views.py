# Django built-in imports
from django.shortcuts import render
from django.contrib.auth.models import Group
# Third party imports
from rest_framework import viewsets
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers
from core import \
        permissions as core_permissions, \
        decorators as core_decorators, \
        responses as core_responses, \
        utils as core_utils
from core.apps.authapp import serializers as authapp_serializers

class DatasheetViewSet(viewsets.GenericViewSet):

    queryset = local_models.Datasheet.objects.all()
    serializer_class = local_serializers.DatasheetCreateSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "operator": "int",
                "lesson": "int",
                "search": "str",
                "status": "str"
            },
            dict(request.query_params)
        )
        filter_model = {
            "operator": "teacher",
            "lesson": "lesson",
            "search": "phone__icontains",
            "status": "status"
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params)
        if request_user.groups.role_id == local_models.User.SUPER_ADMIN:
            datasheets = self.get_queryset().all()
        elif request_user.groups.role_id == local_models.User.ADMIN:
            datasheets = self.get_queryset().filter(
                branch__school=request_user.school, 
                **filter_queries
            )
        elif request_user.groups.role_id == local_models.User.OPERATOR:
            datasheets = self.get_queryset().filter(
                branch=request_user.branch,
                **filter_queries
            )
        p_datasheets = self.paginate_queryset(datasheets)
        datasheets = self.get_serializer_class()(p_datasheets, many=True)
        return self.get_paginated_response(datasheets.data)

    def create(self, request):
        datasheet_request_data = request.data
        datasheet = self.get_serializer_class()(data=datasheet_request_data)
        user = authapp_serializers.CustomUserSerializer(data=datasheet_request_data)
        datasheet.is_valid(raise_exception=True)
        datasheet_request_data["school"] = datasheet.validated_data["branch"].school.id
        datasheet_request_data["groups"] = Group.objects.get(role_id=local_models.User.STUDENT).id
        user.is_valid(raise_exception=True)
        user = user.save()
        datasheet.validated_data["user"] = user
        datasheet.save()
        return core_responses.request_success_with_data(datasheet.data)

    # def put(self, request):
        
