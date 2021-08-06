# Python imports
from calendar import monthrange
from datetime import datetime, timedelta
# Django built-in imports
from django.db.models import Sum
from django.conf import settings
from django.db import transaction as django_transaction
from django.core.files.storage import default_storage
# Third party imports
from rest_framework import viewsets
from rest_framework import decorators as rest_decorator
from rest_framework.response import Response
from rest_framework.settings import api_settings
from storages.backends.s3boto3 import S3Boto3Storage
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        utils as local_utils, \
        services as local_services
from core import \
        responses as core_responses, \
        permissions as core_permissions, \
        decorators as core_decorators, \
        utils as core_utils
from core.apps.studentapp import \
        models as studentapp_models, \
        serializers as studentapp_serializers
        

school_query_model = {
    "school": "branch__school",
    "branch": "branch"
}

class LessonViewSet(viewsets.ModelViewSet):

    queryset = local_models.Lesson.objects.all()
    serializer_class = local_serializers.LessonSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.LessonGetOrModifyPermission,
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
        filter_queries = core_utils.build_filter_query(school_query_model, query_params, user=request_user)
        lessons = local_services.list_lessons(request_user, self.get_queryset(), filter_queries)
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

    def get_serializer_class(self):
        if self.action == "update":
            return local_serializers.LessonUpdateSerializer
        return super().get_serializer_class()

class RoomViewSet(viewsets.ModelViewSet):

    queryset = local_models.Room.objects.all()
    serializer_class = local_serializers.RoomSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.RoomGetOrModifyPermission,
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
        filter_queries = core_utils.build_filter_query(school_query_model, query_params, user=request_user)
        request_user = request.user
        rooms = local_services.list_rooms(request_user, self.get_queryset(), filter_queries)
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

    def get_serializer_class(self):
        if self.action == "update":
            return local_serializers.RoomUpdateSerializer
        return super().get_serializer_class()


class ClassViewSet(viewsets.GenericViewSet):

    queryset = local_models.Class.objects.all()
    serializer_class = local_serializers.ClassDetailSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.ClassGetOrModifyPermission,
        core_permissions.BranchContentManagementPermission,
    ]

    detail_additional_action = [
        "create_calendar",
        "destroy_calendar",
        "list_students",
        "create_student",
        "destroy_student",
        "update_student",
        "list_exams",
        "create_exam",
        "destroy_exam",
        "cancel_student",
    ]

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "teacher": "int",
                "lesson": "int",
                "branch": "int",
                "school": "int",
                "search": "str",
                "status": "str",
            },
            dict(request.query_params)
        )
        today_date = datetime.now()
        filter_model = {
            "teacher": "teacher",
            "lesson": "lesson",
            "search": "name__icontains",
            "branch": "branch",
            "school": "branch__school",
            "status": {
                "active": [
                    {
                        "name": "end_date__gte",
                        "value": today_date
                    },
                    {
                        "name": "start_date__lte",
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
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        classes = local_services.list_classes(request_user, self.get_queryset(), filter_queries)
        p_classes = self.paginate_queryset(classes)
        classes = self.get_serializer_class()(p_classes, many=True, context={ "request": request })
        return self.get_paginated_response(classes.data)

    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def retrieve(self, request, _class=None):
        # __classes = classes.annotate(students_count=Sum("students__discount_amount"))
        # _class = self.get_queryset().filter(id=_class.id).annotate(total_paid=Sum("students__payments__paid")).annotate(total_discount=Sum("students__discount_amount"))
        _class = self.get_queryset().filter(id=_class.id).annotate(total_paid=Sum("students__payments__paid"))
        # _class = self.get_queryset().annotate(total_paid=Sum("students__payments__paid")).filter(id=_class.id)
        _class =_class[0]
        _class = self.get_serializer_class()(_class, context={ "request": request })
        return core_responses.request_success_with_data(_class.data)

    def create(self, request):
        class_request_data = request.data
        _class = self.get_serializer_class()(data=class_request_data)
        _class.is_valid(raise_exception=True)
        _class = _class.save()
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

    @rest_decorator.action(detail=True, methods=[ "GET" ], url_path="calendar")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def list_calendar(self, request, _class=None):
        calendar = _class.calendar.all().order_by("date")
        p_calendar = self.paginate_queryset(calendar)
        calendar = self.get_serializer_class()(p_calendar, many=True)
        return self.get_paginated_response(calendar.data)

    @list_calendar.mapping.post
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    @django_transaction.atomic
    def create_calendar(self, request, _class:local_models.Class=None):
        calendar_data = request.data
        calendar_data["_class"] = _class.id
        calendar = self.get_serializer_class()(data=calendar_data)
        calendar.is_valid(raise_exception=True)
        start_date = calendar.validated_data["date"]
        all_dates = []
        interval = getattr(_class.lesson, "interval", 0)
        if "repeat" in calendar_data and calendar_data["repeat"]:
            for i in range(int((_class.end_date - start_date).days / 7) + 1):
                all_dates.append(start_date)
                start_date += timedelta(days=7)
        else:
            all_dates.append(start_date)
        if interval != None and interval < _class.calendar.count() + len(all_dates):
            return Response({ "detail": "Interval has reached the limit!" }, status=400)
        possible_occupied_date = local_models.Calendar.objects.filter(
            date__in=all_dates,
            room=calendar.validated_data["room"],
            start_time__lte=calendar.validated_data.get("start_time", None),
            end_time__gte=calendar.validated_data.get("start_time", None)
        )
        if possible_occupied_date.exists():
            return Response({ "detail": "Cannot be repeated because room is occupied!" }, status=400)
        for new_date in all_dates:
            new_calendar = local_models.Calendar()
            new_calendar._class = _class
            new_calendar.date = new_date
            new_calendar.room = calendar.validated_data["room"]
            new_calendar.start_time = calendar.validated_data.get("start_time", None)
            new_calendar.end_time = calendar.validated_data.get("end_time", None)
            new_calendar.save()
        return core_responses.request_success()

    @list_calendar.mapping.delete
    @core_decorators.has_key("days")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def destroy_calendar(self, request, _class=None):
        _class.calendar.filter(id__in=request.data["days"]).delete()
        return core_responses.request_success()

    @rest_decorator.action(detail=True, methods=[ "GET" ], url_path="student")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def list_students(self, request, _class=None):
        query_params = core_utils.normalize_data(
            { 
                "status": "str",
                "search": "str"
            },
            dict(request.query_params)
        )
        today_date = datetime.now()
        filter_model = {
            "status": {
                "active": [
                    {
                        "name": "end_date__gte",
                        "value": today_date
                    },
                    {
                        "name": "canceled",
                        "value": False
                    }
                ],
                "completed": [
                    {
                        "name": "end_date__lt",
                        "value": today_date
                    },
                    {
                        "name": "canceled",
                        "value": False
                    }
                ],
                "canceled": {
                    "name": "canceled",
                    "value": True
                }
            },
            "search": "user__phone__startswith"
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params)
        students = _class.students.filter(**filter_queries).annotate(payments_paid=Sum("payments__paid")).order_by("id")
        p_student = self.paginate_queryset(students)
        students = self.get_serializer_class()(p_student, many=True)
        return self.get_paginated_response(students.data)

    @list_students.mapping.post
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

    @list_students.mapping.put
    @core_decorators.has_key("student")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def update_student(self, request, _class=None):
        student_request_data = request.data
        student = studentapp_models.Student.objects.filter(id=request.data["student"])
        if not student.exists():
            return core_responses.request_denied()
        student = self.get_serializer_class()(student[0], data=student_request_data)
        student.is_valid(raise_exception=True)
        class_price = _class.lesson.price
        if "discounts" in student.validated_data:
            student.validated_data["discount_amount"] = local_utils.calculate_discount(class_price, student.validated_data["discounts"])
        student.save()
        return core_responses.request_success_with_data(student.data)

    @rest_decorator.action(detail=True, methods=[ "GET" ], url_path="exam")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def list_exams(self, request, _class=None):
        exams = _class.exams.all()
        exams = self.get_serializer_class()(exams, many=True)
        return core_responses.request_success_with_data(exams.data)

    @list_exams.mapping.post
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def create_exam(self, request, _class=None):
        exam_request_data = request.data
        exam_request_data["_class"] = _class.id
        exam = self.get_serializer_class()(data=exam_request_data)
        exam.is_valid(raise_exception=True)
        exam.save()
        return core_responses.request_success_with_data(exam.data)

    @list_exams.mapping.delete
    @core_decorators.has_key("exams")
    @core_decorators.object_exists(model=local_models.Class, detail="Class")
    def destroy_exam(self, request, _class=None):
        _class.exams.filter(id__in=request.data["exams"]).delete()
        return core_responses.request_success()

    def get_serializer_class(self):
        if self.action == "update" or self.action == "create":
            return local_serializers.ClassCreateAndUpdateSerializer
        elif self.action == "retrieve":
            return local_serializers.ClassFullDetailSerializer
        elif self.action == "create_calendar":
            return local_serializers.CalendarSerializer
        elif self.action == "list_calendar":
            return local_serializers.CalendarSerializer
        elif self.action == "create_student":
            return studentapp_serializers.StudentCreateSerializer
        elif self.action == "update_student":
            return studentapp_serializers.StudentUpdateSerializer
        elif self.action == "list_students":
            return studentapp_serializers.StudentShortDetailSerializer
        elif self.action in [ "list_exams", "create_exam" ]:
            return local_serializers.ExamSerializer
        elif self.action == "update_exam":
            return local_serializers.ExamUpdateSerializer
        else:
            return super(ClassViewSet, self).get_serializer_class()


class CalendarViewSet(viewsets.GenericViewSet):

    queryset = local_models.Calendar.objects.all()
    serializer_class = local_serializers.CalendarSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.CalendarGetOrModifyPermission
    ]

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "branch": "int",
                "school": "int",
                "teacher": "int",
                "room": "int",
                "filter": "str",
                "year": "int",
                "month": "int",
            },
            dict(request.query_params)
        )
        today_date = datetime.now()
        month = query_params.get("month", today_date.month)
        year = query_params.get("year", today_date.year)
        month_date = datetime(2021, month, monthrange(year, month)[1])
        filter_model = {
            "school": "_class__branch__school",
            "branch": "_class__branch",
            "teacher": "_class__teacher",
            "room": "room",
            "filter": {
                "month": [
                    {
                        "name": "_class__start_date__lte",
                        "value": month_date
                    },
                    {
                        "name": "_class__end_date__year",
                        "value": year
                    },
                    {
                        "name": "_class__end_date__month__gte",
                        "value": month
                    }
                ]
            }
        }
        filter_queries = core_utils.build_filter_query(
            filter_model, 
            query_params, 
            user=request_user
        )
        if request_user.groups.role_id == local_models.User.SUPER_ADMIN:
            calendar = self.get_queryset().filter(**filter_queries)
        elif request_user.groups.role_id == local_models.User.ADMIN:
            calendar = self.get_queryset().filter(_class__branch__school=request_user.school.id, **filter_queries)
        elif request_user.groups.role_id == local_models.User.TEACHER:
            calendar = self.get_queryset().filter(_class__teacher=request_user, **filter_queries)
        else:
            calendar = self.get_queryset().filter(_class__branch=request_user.branch, **filter_queries)
        p_calendar = self.paginate_queryset(calendar)
        calendar = self.get_serializer_class()(p_calendar, many=True)
        return self.get_paginated_response(calendar.data)

    @core_decorators.object_exists(model=local_models.Calendar, detail="Calendar")
    def update(self, request, calendar):
        calendar_data = request.data
        calendar = self.get_serializer_class()(calendar, data=calendar_data)
        calendar.is_valid(raise_exception=True)
        calendar.save()
        return core_responses.request_success_with_data(calendar.data)


class ExamViewSet(viewsets.GenericViewSet):

    queryset = local_models.Exam
    serializer_class = local_serializers.ExamUpdateSerializer

    @core_decorators.object_exists(model=local_models.Exam, detail="Exam")
    @core_decorators.has_access_to_class
    def update(self, request, exam=None):
        exam_request_data = request.data
        exam = self.get_serializer_class()(exam, data=exam_request_data)
        exam.is_valid(raise_exception=True)
        exam.save()
        return core_responses.request_success_with_data(exam.data)

    @rest_decorator.action(detail=True, methods=[ "POST" ], url_path="result")
    @core_decorators.object_exists(model=local_models.Exam, detail="Exam")
    @core_decorators.has_access_to_class
    def create_exam_result(self, request, exam=None):
        exam_result_request_data = request.data
        exam_result_request_data["exam"] = exam.id
        exam_result = studentapp_serializers.ExamResultSerializer(data=exam_result_request_data)
        exam_result.is_valid(raise_exception=True)
        exam_result.save()
        return core_responses.request_success_with_data(exam_result.data)

    @create_exam_result.mapping.put
    @core_decorators.has_keys("id", "mark")
    @core_decorators.object_exists(model=local_models.Exam, detail="Exam")
    @core_decorators.has_access_to_class
    def update_exam_result(self, request, exam=None):
        exam_result = exam.results.filter(id=request.data["id"])
        if not exam_result.exists():
            return core_responses.request_denied()
        mark = request.data["mark"]
        if type(mark).__name__ != "int":
            return core_responses.request_denied()
        exam_result = exam_result[0]
        exam_result.mark = mark
        exam_result.save()
        return core_responses.request_success()


class Curriculum(viewsets.GenericViewSet):

    queryset = local_models.Curriculum.objects.all()
    serializer_class = local_serializers.CurriculumSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.CurriculumGetOrModifySerializer,
        core_permissions.SchoolContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "search": "str",
                "school": "int"
            },
            dict(request.query_params)
        )
        filter_model = {
            "search": "name__contains",
            "school": "school"
        }
        filter_queries = core_utils.build_filter_query(filter_model, query_params, user=request_user)
        curriculums = local_services.list_curriculums(request_user, self.get_queryset(), filter_queries)
        p_curriculums = self.paginate_queryset(curriculums)
        curriculums = local_serializers.CurriculumSerializer(p_curriculums, many=True, context={ "request": request })
        return self.get_paginated_response(curriculums.data)

    def create(self, request):
        curriculum_data = request.data
        curriculum_data = self.get_serializer_class()(data=curriculum_data)
        curriculum_data.is_valid(raise_exception=True)
        curriculum_data.save()
        return core_responses.request_success()

    def retrieve(self, request, pk=None):
        return core_responses.request_success()

    @core_decorators.object_exists(model=local_models.Curriculum, detail="Curriculum")
    def update(self, request, curriculum=None):
        curriculum_data = request.data
        _curriculum = self.get_serializer_class()(curriculum, data=curriculum_data)
        _curriculum.is_valid(raise_exception=True)
        _curriculum.save()
        return core_responses.request_success_with_data(_curriculum.data)

    @core_decorators.object_exists(model=local_models.Curriculum, detail="Curriculum")
    def delete(self, request, curriculum=None):
        curriculum.delete()
        return core_responses.request_success()

    @rest_decorator.action(detail=True, methods=[ "GET" ], url_path="file")
    @core_decorators.object_exists(model=local_models.Curriculum, detail="Curriculum")
    def get_curriculum_file(self, request, curriculum=None):
        config = {}
        if settings.SERVER_PRODUCTION == 1:
            config["expire"] = 10
        signed_url = default_storage.url(curriculum.file.name, **config)
        data = {
            "name": curriculum.name,
            "url": signed_url
        }
        return core_responses.request_success_with_data(data)

    def get_serializer_class(self):
        if self.action == "update":
            return local_serializers.CurriculumUpdateSerializer
        return super().get_serializer_class()