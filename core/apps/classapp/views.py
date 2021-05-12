# Python imports
from datetime import datetime
# Django built-in imports
from django.shortcuts import render
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import viewsets
from rest_framework import decorators as rest_decorator
from rest_framework.response import Response
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        utils as local_utils
from core import \
        responses as core_responses, \
        permissions as core_permissions, \
        decorators as core_decorators, \
        utils as core_utils
from core.apps.studentapp import \
        models as studentapp_models, \
        serializers as studentapp_serializers

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
        # core_permissions.ClassGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "teacher": "int",
                "lesson": "int",
                "search": "str",
                "status": "str"
            },
            dict(request.query_params)
        )
        today_date = datetime.now()
        filter_model = {
            "teacher": "teacher",
            "lesson": "lesson",
            "search": "name__icontains",
            "status": {
                "active": [
                    {
                        "name": "end_date__gte",
                        "value": today_date
                    },
                    {
                        "name": "start_date__lt",
                        "value": today_date
                    }
                ],
                "finished": {
                    "name": "end_date__lt",
                    "value": today_date
                },
                "soon": {
                    "name": "start_date__gt",
                    "value": today_date
                }
            }
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params)
        if request_user.groups.role_id == User.SUPER_ADMIN:
            classes = self.get_queryset().all()
        elif request_user.groups.role_id == User.ADMIN:
            branches = request_user.school.branches.all()
            classes = self.get_queryset().filter(
                branch__in=branches, 
                **filter_queries
            )
        elif request_user.groups.role_id == User.OPERATOR:
            classes = self.get_queryset().filter(
                branch=request_user.branch, 
                **filter_queries
            )
        elif request_user.groups.role_id == User.TEACHER:
            classes = self.get_queryset().filter(
                teacher=request_user, 
                **filter_queries
            )
        p_classes = self.paginate_queryset(classes)
        classes = self.get_serializer_class()(p_classes, many=True)
        return self.get_paginated_response(classes.data)

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def retrieve(self, request, _class=None):
        _class = self.get_serializer_class()(_class)
        return core_responses.request_success_with_data(_class.data)

    def create(self, request):
        class_request_data = request.data
        _class = self.get_serializer_class()(data=class_request_data)
        _class.is_valid(raise_exception=True)
        # _class = _class.save()
        return core_responses.request_success()

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def destroy(self, request, _class=None):
        _class.delete()
        return core_responses.request_success()

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def update(self, request, _class=None):
        class_requst_data = request.data
        upd_class = self.get_serializer_class()(_class, data=class_requst_data)
        upd_class.is_valid(raise_exception=True)
        upd_class.save()
        return core_responses.request_success_with_data(upd_class.data)

    @rest_decorator.action(detail=True, methods=[ "POST" ], url_path="calendar")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def create_calendar(self, request, _class=None):
        calendar_request_data = request.data
        calendar_request_data["_class"] = _class.id
        calendar = self.get_serializer_class()(data=calendar_request_data, many=True)
        calendar.is_valid(raise_exception=True)
        calendar.save()
        return core_responses.request_success_with_data(calendar.data)

    @create_calendar.mapping.delete
    @core_decorators.has_key("days")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def destroy_calendar(self, request, _class=None):
        _class.calendar.filter(id__in=request.data["days"]).delete()
        return core_responses.request_success()

    @rest_decorator.action(detail=True, methods=[ "POST" ], url_path="student")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def create_student(self, request, _class=None):
        student_request_data = request.data
        student_request_data["operator"] = request.user.id
        student_request_data["_class"] = _class.id
        student = self.get_serializer_class()(data=student_request_data)
        student.is_valid(raise_exception=True)
        class_price = _class.lesson.price
        if "discounts" in student.validated_data:
            student.validated_data["discount_amount"] = local_utils.calculate_discount(class_price, student.validated_data["discounts"])
        student.save()
        return core_responses.request_success_with_data(student.data)

    @create_student.mapping.put
    @core_decorators.has_key("user")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def update_student(self, request, _class=None):
        student_request_data = request.data
        student = studentapp_models.Student.objects.filter(user=request.data["user"])
        if not student.exists():
            return core_responses.request_denied()
        student = self.get_serializer_class()(student[0], data=student_request_data)
        student.is_valid(raise_exception=True)
        class_price = _class.lesson.price
        if "discounts" in student.validated_data:
            student.validated_data["discount_amount"] = local_utils.calculate_discount(class_price, student.validated_data["discounts"])
        student.save()
        return core_responses.request_success_with_data(student.data)

    @rest_decorator.action(detail=True, methods=[ "POST" ], url_path="student/datasheet")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def create_student_from_datasheet(self, request, _class=None):
        student_request_data = request.data
        student_request_data["operator"] = request.user.id
        student_request_data["_class"] = _class.id
        student = self.get_serializer_class()(data=student_request_data)
        student.is_valid(raise_exception=True)
        class_price = student.validated_data["_class"].lesson.price
        student.validated_data["discount_amount"] = local_utils.calculate_discount(class_price, student.validated_data["discounts"])
        student.save()
        return core_responses.request_success_with_data(student.data)

    def get_serializer_class(self):
        if self.action == "update" or self.action == "create":
            return local_serializers.ClassCreateAndUpdateSerializer
        elif self.action == "retrieve":
            return local_serializers.ClassFullDetailSerializer
        elif self.action == "create_calendar":
            return local_serializers.CalendarSerializer
        elif self.action == "create_student":
            return studentapp_serializers.StudentCreateSerializer
        elif self.action == "update_student":
            return studentapp_serializers.StudentUpdateSerializer
        else:
            return super(ClassViewSet, self).get_serializer_class()


class CalendarViewSet(viewsets.GenericViewSet):

    queryset = local_models.Calendar.objects.all()
    serializer_class = local_serializers.CalendarSerializer

    def list(self, request):
        request_user = request.user
        if request_user.groups.role_id == User.SUPER_ADMIN:
            calendar = self.get_queryset().all()
        elif request_user.groups.role_id == User.ADMIN:
            branches = request_user.school.branches.all()
            calendar = self.get_queryset().filter(_class__branch__in=branches)
        elif request_user.groups.role_id == User.OPERATOR:
            calendar = self.get_queryset().filter(_class__branch=request_user.branch)
        elif request_user.groups.role_id == User.TEACHER:
            calendar = self.get_queryset().filter(_class__teacher=request_user)
        p_calendar = self.paginate_queryset(calendar)
        calendar = self.get_serializer_class()(p_calendar, many=True)
        return self.get_paginated_response(calendar.data)
    