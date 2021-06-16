# Python imports
from datetime import datetime, timedelta
# Django built-in imports
from django.shortcuts import render
from django.contrib.auth.models import Group
# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        services as local_services
from core import \
        permissions as core_permissions, \
        decorators as core_decorators, \
        responses as core_responses, \
        utils as core_utils
from core.apps.authapp import serializers as authapp_serializers

school_query_model = {
    "school": "branch__school",
    "branch": "branch"
}

class DatasheetViewSet(viewsets.GenericViewSet):

    queryset = local_models.Datasheet.objects.all()
    serializer_class = local_serializers.DatasheetCreateSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.DatasheetGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]
    pagination_class = None

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "operator": "int",
                "lesson": "int",
                "search": "str",
                "status": "str",
                "branch": "int",
                "school": "int",
                "day": "int",
                "date": "str"
            },
            dict(request.query_params)
        )
        today_date = datetime.now()
        filter_model = {
            "operator": "operator",
            "lesson": "lesson",
            "search": "user__phone__startswith",
            "status": "status",
            "branch": "branch",
            "school": "branch__school",
            "day": {
                1: {
                    "name": "created__gte",
                    "value": today_date - timedelta(days=1)
                },
                3: {
                    "name": "created__gte",
                    "value": today_date - timedelta(days=3)
                },
                7: {
                    "name": "created__gte",
                    "value": today_date - timedelta(days=7)
                },
                -1: {
                    "name": "created",
                    "value": query_params.get("date", "2001-05-20")
                }
            }
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params)
        datasheets = local_services.list_datasheet(request_user, self.get_queryset(), filter_queries)
        datasheets = self.get_serializer_class()(datasheets, many=True)
        return core_responses.request_success_with_data(datasheets.data)

    def create(self, request, pk=None):
        datasheet_request_data = request.data
        datasheet = self.get_serializer_class()(data=datasheet_request_data)
        datasheet.is_valid(raise_exception=True)
        if "user" not in datasheet_request_data:
            datasheet_request_data["school"] = datasheet.validated_data["branch"].school.id
            datasheet_request_data["groups"] = Group.objects.get(role_id=local_models.User.STUDENT).id
            datasheet_request_data["seen_datasheet"] = local_models.User.CREATED_FROM_DATASHEET
            user = authapp_serializers.CustomUserSerializer(data=datasheet_request_data, user=request.user)
            user.is_valid(raise_exception=True)
            user = user.save()
            datasheet.validated_data["user"] = user
        else:
            user = datasheet.validated_data["user"]
            if user.students.exists():
                user.seen_datasheet = local_models.User.DATASHEET_AND_STUDENT
        datasheet.save()
        return core_responses.request_success_with_data(datasheet.data)

    @core_decorators.object_exists(model=local_models.Datasheet, detail="Datasheet")
    def update(self, request, datasheet=None):
        datasheet_request_data = request.data
        _datasheet = self.get_serializer_class()(datasheet, data=datasheet_request_data)
        _datasheet.is_valid(raise_exception=True)
        if "with_user" in datasheet_request_data:
            user = authapp_serializers.CustomUserUpdateSerializer(datasheet.user, data=datasheet_request_data, user=request.user)
            user.is_valid(raise_exception=True)
            user = user.save()
        _datasheet.save()
        return core_responses.request_success()

    @core_decorators.object_exists(model=local_models.Datasheet, detail="Datasheet")
    def destroy(self, request, datasheet=None):
        datasheet.user.delete()
        return core_responses.request_success()

    def get_serializer_class(self):
        if self.action == "update":
            return local_serializers.DatasheetUpdateSerializer
        return super().get_serializer_class()


class DatasheetStatusViewSet(viewsets.ModelViewSet):

    queryset = local_models.Status.objects.all()
    serializer_class = local_serializers.DatasheetStatusSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.DatasheetStatusGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "school": "int",
                "branch": "int"
            },
            dict(request.query_params)
        )
        filter_queries = core_utils.build_filter_query(school_query_model, query_params)
        datasheet_status = local_services.list_datasheet_status(request_user, self.get_queryset(), filter_queries=filter_queries)
        p_datasheet_status = self.paginate_queryset(datasheet_status)
        datasheet_status = self.get_serializer_class()(p_datasheet_status, many=True)
        return self.get_paginated_response(datasheet_status.data)

    @core_decorators.object_exists(model=local_models.Status, detail="Status")
    def retrieve(self, request, status=None):
        data = super(DatasheetStatusViewSet, self).retrieve(request, status.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(DatasheetStatusViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Status, detail="Status")
    def update(self, request, status=None):
        data = super(DatasheetStatusViewSet, self).update(request, status.id).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Status, detail="Status")
    def destroy(self, request, status=None):
        super(DatasheetStatusViewSet, self).destroy(request, status.id)
        return core_responses.request_success()
    
    def get_serializer_class(self):
        if self.action == "update":
            return local_serializers.DatasheetStatusUpdateSerializer
        return super().get_serializer_class()