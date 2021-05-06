# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
# Local imports
from . import models as local_models, serializers as local_serializers
from core import \
    decorators as core_decorators, \
    permissions as core_permissions, \
    responses as core_responses

# User model
User = get_user_model()

class SchoolViewSet(viewsets.ModelViewSet):

    queryset = local_models.School.objects.all()
    serializer_class =  local_serializers.SchoolSerializer
    parser_classes = [ MultiPartParser, FormParser, FileUploadParser ]
    permission_classes = [ core_permissions.SchoolGetOrModifyPermission, ]

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

    


class BranchViewSet(viewsets.GenericViewSet):

    queryset = local_models.Branch.objects.all()
    serializer_class = local_serializers.BranchSerializer
    # parser_classes = [ MultiPartParser, FormParser, FileUploadParser ]
    
    def list(self, request):
        request_user = request.user
        branches = []
        if request_user.groups.id is User.SUPER_ADMIN:
            branches = self.get_queryset().all() 
        elif request_user.groups.id is User.ADMIN:
            branches = self.get_queryset().filter(school=request_user.school)
        p_branches = self.paginate_queryset(branches)
        branches = self.get_serializer_class()(p_branches, many=True)
        return self.get_paginated_response(branches.data)

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(Self, request, pk=None):
        pass

    def retrieve(self, request, pk=None):
        pass

