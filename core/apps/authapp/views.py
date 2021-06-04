# Django built-in imports
from django.db.models.fields import CharField
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Sum, F
# Third party imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        services as local_services
from core import \
        decorators as core_decorators, \
        permissions as core_permissions, \
        responses as core_responses, \
        utils as core_utils

# User Model
User = get_user_model()

class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = local_serializers.CustomUserSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.UserGetOrModifyPermission,
        core_permissions.SchoolContentManagementPermission,
        core_permissions.BranchContentManagementPermission
    ]

    @action(detail=True, methods=[ "GET" ])
    @core_decorators.object_exists(model=Group, detail="Group", field="role_id")
    def group(self, request, groups=None):
        request_user = request.user
        users = local_services.list_users(request_user, self.get_queryset(), groups=groups.role_id)
        if groups.role_id == User.TEACHER:
            users = users.annotate(job_hour=Sum(F("classes__calendar__end_time") - F("classes__calendar__start_time"), output_field=CharField())).order_by("id")
        p_users = self.paginate_queryset(users)
        users = self.get_serializer_class()(p_users, many=True)
        return self.get_paginated_response(users.data)

    @core_decorators.object_exists(model=User, detail="User")
    def retrieve(self, request, user):
        request_user = request.user
        if not core_utils.check_if_user_can_procceed(request_user, user.school.id, user.branch.id):
            return core_responses.request_denied()
        user = self.get_serializer_class()(user)
        return core_responses.request_success_with_data(user.data)

    def create(self, request):
        user_request_data = request.data
        user = self.get_serializer_class()(data=user_request_data, user=request.user)
        user.is_valid(raise_exception=True)
        # if request_user.groups.role_id >= int(user_request_data["groups"]):
        #     return core_responses.request_denied()
        user = user.save()
        profile = local_serializers.UserProfileSerializer(user.profile, data=user_request_data)
        profile.is_valid(raise_exception=True)
        profile.save()
        user = self.get_serializer_class()(user, many=False)
        return core_responses.request_success_with_data(user.data)

    @core_decorators.object_exists(model=User, detail="User")
    def destroy(self, request, user=None):
        if request.user.groups.role_id >= user.groups.role_id:
            return core_responses.request_denied()
        user.is_active = False
        user.save()
        return core_responses.request_success()

    @core_decorators.object_exists(model=User, detail="User")
    def update(self, request, user=None):
        if (request.user.id is not user.id and 
            (request.user.groups.role_id >= user.groups.role_id or 
             request.user.groups.role_id >= User.OPERATOR)):
            return core_responses.request_denied()
        user_request_data = request.data
        upd_user = self.get_serializer_class()(user, data=user_request_data)
        upd_user.is_valid(raise_exception=True)
        user_request_data["user"] = user.id
        upd_profile = local_serializers.UserProfileSerializer(user.profile, data=user_request_data)
        upd_profile.is_valid(raise_exception=True)
        upd_profile.save()       
        upd_user.save()
        return core_responses.request_success_with_data(upd_user.data)
        
