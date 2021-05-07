# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
# Local imports
from . import models as local_models
from . import serializers as local_serializers
from core import \
        responses as core_responses, \
        permissions as core_permissions, \
        decorators as core_decorators

# User model
User = get_user_model()

class LessonViewSet(viewsets.ModelViewSet):

    queryset = local_models.Lesson.objects.all()
    serializer_class = local_serializers.LessonSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.LessonGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        if request_user.groups.role_id == User.SUPER_ADMIN:
            lessons = self.get_queryset().all()
        elif request_user.groups.role_id == User.ADMIN:
            branches = request_user.school.branches.all()
            lessons = self.get_queryset().filter(branch__in=branches)
        elif request_user.groups.role_id == User.OPERATOR:
            lessons = self.get_queryset().filter(branch=request_user.branch)
        p_lessons = self.paginate_queryset(lessons)
        lessons = self.get_serializer_class()(p_lessons, many=True)
        return self.get_paginated_response(lessons.data)

    @core_decorators.object_exists(model=local_models.Lesson, detail="Lesson")
    def retrieve(self, request, lesson=None):
        data = super(LessonViewSet, self).retrieve(request, lesson.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(LessonViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Lesson, detail="Lesson")
    def update(self, request, lesson=None):
        data = super(LessonViewSet, self).update(request, lesson.id).data
        return core_responses.request_success_with_data(data)


class RoomViewSet(viewsets.ModelViewSet):

    queryset = local_models.Room.objects.all()
    serializer_class = local_serializers.RoomSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.RoomGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        if request_user.groups.role_id == User.SUPER_ADMIN:
            rooms = self.get_queryset().all()
        elif request_user.groups.role_id == User.ADMIN:
            branches = request_user.school.branches.all()
            rooms = self.get_queryset().filter(branch__in=branches)
        elif request_user.groups.role_id == User.OPERATOR:
            rooms = self.get_queryset().filter(branch=request_user.branch)
        p_rooms = self.paginate_queryset(rooms)
        rooms = self.get_serializer_class()(p_rooms, many=True)
        return self.get_paginated_response(rooms.data)

    @core_decorators.object_exists(model=local_models.Room, detail="Lesson")
    def retrieve(self, request, room=None):
        data = super(RoomViewSet, self).retrieve(request, room.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(RoomViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Room, detail="Lesson")
    def update(self, request, room=None):
        data = super(RoomViewSet, self).update(request, room.id).data
        return core_responses.request_success_with_data(data)


class ClassViewSet(viewsets.GenericViewSet):

    queryset = local_models.Class.objects.all()
    serializer_class = local_serializers.ClassDetailSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        if request_user.groups.role_id == User.SUPER_ADMIN:
            classes = self.get_queryset().all()
        elif request_user.groups.role_id == User.ADMIN:
            branches = request_user.school.branches.all()
            classes = self.get_queryset().filter(branch__in=branches)
        elif request_user.groups.role_id == User.OPERATOR:
            classes = self.get_queryset().filter(branch=request_user.branch)
        elif request_user.groups.role_id == User.TEACHER:
            classes = self.get_queryset().filter(teacher=request_user)
        p_classes = self.paginate_queryset(classes)
        classes = self.get_serializer_class()(p_classes, many=True)
        return self.get_paginated_response(classes.data)

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def retrieve(self, request, _class=None):
        _class = self.get_serializer_class()(_class)
        return core_responses.request_success_with_data(_class.data)

    def create(self, request):
        class_request_data = request.data
        _class = local_serializers.ClassCreateAndUpdateSerializer(data=class_request_data)
        _class.is_valid(raise_exception=True)
        # _class.save()
        return core_responses.request_success()

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def destroy(self, request, _class=None):
        _class.delete()
        return core_responses.request_success()

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def update(self, request, _class=None):
        pass