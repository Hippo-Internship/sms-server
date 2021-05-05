# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
# Local imports
from . import models as local_models, serializers as local_serializers
from core import decorators as core_decorators

# User Model
User = get_user_model()

class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = local_serializers.CustomUserSerializer

    @core_decorators.object_exists(model=Group, detail="Group")
    def retrieve(self, request, group):
        if request.user.group.id > group.id:
            return Response({ "detail": "Request Denied!", "success": False })
        users = group.customuser_set.all()
        p_users = self.paginate_queryset(users)
        users = self.get_serializer_class()(p_users, many=True)
        return self.get_paginated_response(users.data);

    def create(self, request):
        user_request_data = request.data
        user = self.get_serializer_class()(data=user_request_data)
        user.is_valid(raise_exception=True)
        if user_request_data["group"] < request.user.group.id:
            return Response({ "detail": "Request Denied!", "success": False })
        user = user.save()
        user_request_data["user"] = user.id
        profile = local_serializers.UserProfileSerializer(data=user_request_data)
        profile.is_valid(raise_exception=True)
        profile.save()
        user = self.get_serializer_class()(user, many=False)
        return Response({ "data": user.data, "success": True })


    @core_decorators.object_exists(model=User, detail="User")
    def destroy(self, request, user=None):
        if request.user.group.id > user.group.id:
            return Response({ "detail": "Request Denied!", "success": False })
        user.delete()
        return Response({ "success": True })


    @core_decorators.object_exists(model=User, detail="User")
    def update(self, request, user=None):
        if request.user.group.id > user.group.id:
            return Response({ "detail": "Request Denied!", "success": False })
        user_request_data = request.data
        upd_user = self.get_serializer_class()(user, data=user_request_data)
        upd_user.is_valid(raise_exception=True)
        user_request_data["user"] = user.id
        upd_profile = local_serializers.UserProfileSerializer(user.profile, data=user_request_data)
        upd_profile.is_valid(raise_exception=True)
        upd_profile.save()       
        upd_user.save()
        return Response({ "data": upd_user.data, "success": True })
        
