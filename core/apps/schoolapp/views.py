# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import viewsets
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
# Local imports
from . import models as local_models, serializers as local_serializers
from core import \
    decorators as core_decorators, \
    permissions as core_permissions, \
    responses as core_responses, \
    utils as core_utils

# User model
User = get_user_model()

class SchoolViewSet(viewsets.ModelViewSet):

    queryset = local_models.School.objects.all()
    serializer_class =  local_serializers.SchoolSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.SchoolGetOrModifyPermission
    ]

    @core_decorators.object_exists(model=local_models.School, detail="School")
    def retrieve(self, request, school):
        data = super(SchoolViewSet, self).retrieve(request, school.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(SchoolViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.School, detail="School")
    def update(self, request, school=None):
        data = super(SchoolViewSet, self).update(request, school.id).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.School, detail="School")
    def destroy(self, request, school=None):
        super(SchoolViewSet, self).destroy(request, school.id)
        return core_responses.request_success()

    
class BranchViewSet(viewsets.GenericViewSet):

    queryset = local_models.Branch.objects.all()
    serializer_class = local_serializers.BranchSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.BranchGetOrModifyPermission,
        core_permissions.SchoolContentManagementPermission,
    ]
    
    def list(self, request):
        request_user = request.user
        branches = []
        if request_user.groups.role_id is User.SUPER_ADMIN:
            branches = self.get_queryset().all() 
        elif request_user.groups.role_id is User.ADMIN:
            branches = self.get_queryset().filter(school=request_user.school)
        p_branches = self.paginate_queryset(branches)
        branches = self.get_serializer_class()(p_branches, many=True)
        return self.get_paginated_response(branches.data)

    def create(self, request):
        request_user = request.user
        branch_request_data = request.data
        branch = self.get_serializer_class()(data=branch_request_data)
        branch.is_valid(raise_exception=True)
        branch.save()
        return core_responses.request_success_with_data(branch.data)

    @core_decorators.object_exists(model=local_models.Branch, detail="Branch")
    def update(self, request, branch=None):
        request_user = request.user
        branch_request_data = request.data
        s_branch = self.get_serializer_class()(branch, data=branch_request_data)
        s_branch.is_valid(raise_exception=True)
        if branch.school.id == branch_request_data["school"]:
            return core_responses.request_denied()
        s_branch.save()
        return core_responses.request_success_with_data(s_branch.data)

    @core_decorators.object_exists(model=local_models.Branch, detail="Branch")
    def destroy(Self, request, branch=None):
        request_user = request.user
        branch.delete()
        return core_responses.request_success()

    def retrieve(self, request, pk=None):
        pass

