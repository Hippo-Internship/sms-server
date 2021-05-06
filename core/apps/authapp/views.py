# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Third party imports
from rest_framework import viewsets
from rest_framework.settings import api_settings
from rest_framework.response import Response
# Local imports
from . import models as local_models, serializers as local_serializers
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
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ core_permissions.UserGetOrModifyPermission ]

    @core_decorators.object_exists(model=Group, detail="Group")
    def retrieve(self, request, groups):
        request_user = request.user
        if request_user.groups.id > groups.id:
            return core_responses.request_denied()
        if request_user.groups.id == local_models.CustomUser.ADMIN:
            users = request_user.school.users.filter(groups=groups)
        else:
            users = request_user.branch.users.filter(groups=groups)
        p_users = self.paginate_queryset(users)
        users = self.get_serializer_class()(p_users, many=True)
        return self.get_paginated_response(users.data);

    def create(self, request):
        request_user = request.user
        user_request_data = request.data
        user = self.get_serializer_class()(data=user_request_data)
        user.is_valid(raise_exception=True)
        if request_user.groups.id >= user_request_data["groups"]:
            return core_responses.request_denied()
        if not core_utils.check_if_user_can_procceed(request_user, user_request_data["school"], user_request_data["branch"]):
            return core_responses.request_denied()
        user = user.save()
        print(user.id)
        user_request_data["user"] = user.id
        profile = local_serializers.UserProfileSerializer(data=user_request_data)
        profile.is_valid(raise_exception=True)
        profile.save()
        user = self.get_serializer_class()(user, many=False)
        return core_responses.request_success_with_data(user.data)

    @core_decorators.object_exists(model=User, detail="User")
    def destroy(self, request, user=None):
        if user.groups is not None and request.user.groups.id >= user.groups.id:
            return core_responses.request_denied()
        if not core_utils.check_if_user_can_procceed(request.user, user.schoo.id, user.branch.id):
            return core_responses.request_denied()
        user.delete()
        return core_responses.request_success()

    @core_decorators.object_exists(model=User, detail="User")
    def update(self, request, user=None):
        if request.user.id is not user.id and request.user.groups.id >= user.groups.id:
            return core_responses.request_denied()
        if not core_utils.check_if_user_can_procceed(request.user, user.school.id, user.branch.id):
            return core_responses.request_denied()
        user_request_data = request.data
        upd_user = local_serializers.CustomUserUpdateSerializer(user, data=user_request_data)
        upd_user.is_valid(raise_exception=True)
        user_request_data["user"] = user.id
        upd_profile = local_serializers.UserProfileSerializer(user.profile, data=user_request_data)
        upd_profile.is_valid(raise_exception=True)
        upd_profile.save()       
        upd_user.save()
        return core_responses.request_success_with_data(upd_user.data)
        
