# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
# Local imports
from . import models as local_models, serializers as local_serializers
from core import decorators as core_decorators

class UserViewSet(viewsets.GenericViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = local_serializers.CustomUserSerializer

    def list(self, request):
        
        pass

    def create(self, request):
        user_request_data = request.data
        user = self.get_serializer_class()(data=user_request_data)
        user.is_valid(raise_exception=True)
        if user_request_data["role_id"] <= 2:
            return Response({ "detail": "Request Denied!", "success": False })
        user = user.save()
        user_request_data["user"] = user.id
        profile = local_serializers.UserProfileSerializer(data=user_request_data)
        profile.is_valid(raise_exception=True)
        profile.save()
        user = self.get_serializer_class()(user, many=False)
        return Response({ "data": user.data, "success": True })

    @core_decorators.object_exists(model=get_user_model(), detail="User")
    def destroy(self, request, user=None):
        if user.role <= 2:
            return Response({ "detail": "Request Denied!", "success": False })
        user.delete()
        return Response({ "success": True })
        
