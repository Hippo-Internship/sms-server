# Python imports
from datetime import datetime
# Django built-in imports
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count, Sum
from django.db.models import Q
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
# Local imports
from . import models as local_models
from core.apps.authapp import serializers as authapp_serializers
from core.apps.schoolapp import serializers as schoolapp_serializers

# User model
User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Lesson
        fields = "__all__"

class LessonUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Lesson
        fields = "__all__"
        extra_kwargs = {
            "branch": { "read_only": True }
        }


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Room
        fields = "__all__"


class RoomUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Room
        fields = "__all__"
        extra_kwargs = {
            "branch": { "read_only": True }
        }


class ClassCreateAndUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Class
        fields = "__all__"
        extra_kwargs = {
            "lesson": { "required": True },
            "teacher": { "required": True },
            "room": { "required": True },
        }

    def validate_lesson(self, value):
        if value.branch.id != self.initial_data.get("branch", 0):
            raise PermissionDenied()
        if not value.is_active:
            raise serializers.ValidationError("Lesson doesn't exist!")
        return value

    def validate_teacher(self, value):
        if value.branch.id != self.initial_data.get("branch", 0):
            raise PermissionDenied()
        if value.groups.role_id != User.TEACHER:
            raise serializers.ValidationError("Invalid teacher!")
        if not value.is_active:
            raise serializers.ValidationError("Teacher doesn't exist!")
        return value

    def validate_end_date(self, value):
        initial_data = self.initial_data
        start_date = initial_data.get("start_date", None)
        end_date = initial_data.get("end_date", None)
        if end_date < start_date:
            raise serializers.ValidationError("End date should be later than the start date!")
        return value

    def validate_end_time(self, value):
        initial_data = self.initial_data
        start_time = initial_data.get("start_time", None)
        end_time = initial_data.get("end_time", None)
        if start_time > end_time:
            raise serializers.ValidationError("End time should be later than the start time!")
        return value


class ClassDetailSerializer(serializers.ModelSerializer):

    branch_name = serializers.CharField(source="branch.name", read_only=True)
    teacher_firstname = serializers.CharField(source="teacher.firstname", read_only=True)
    teacher_lastname = serializers.CharField(source="teacher.lastname", read_only=True)
    lesson_name = serializers.CharField(source="lesson.name", read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    total_paid = serializers.IntegerField(read_only=True)
    branch_image = serializers.ImageField(source="branch.image", read_only=True)

    class Meta:
        model = local_models.Class
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Exam
        fields = "__all__"

    def validate_date(self, value):
        if value < datetime.date(datetime.now()):
            raise serializers.ValidationError("Start date should be later than the today's date!")
        return value


class ClassFullDetailSerializer(serializers.ModelSerializer):

    teacher_firstname = serializers.CharField(source="teacher.firstname", read_only=True)
    teacher_lastname = serializers.CharField(source="teacher.lastname", read_only=True)
    teacher_is_active = serializers.BooleanField(source="teacher.is_active", read_only=True)
    lesson_name = serializers.CharField(source="lesson.name", read_only=True)
    lesson_price = serializers.IntegerField(source="lesson.price", read_only=True)
    lesson_color = serializers.CharField(source="lesson.color", read_only=True)
    lesson_interval = serializers.CharField(source="lesson.interval", read_only=True)
    lesson_exam = serializers.CharField(source="lesson.exam", read_only=True)
    lesson_desc = serializers.CharField(source="lesson.description", read_only=True)
    lesson_is_active = serializers.CharField(source="lesson.is_active", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)
    total_paid = serializers.IntegerField(read_only=True)
    total_discount = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.ReadOnlyField()
    school = serializers.IntegerField(source="branch.school.id", read_only=True)
    branch_image = serializers.ImageField(source="branch.image", read_only=True)

    class Meta:
        model = local_models.Class
        fields = "__all__"

    def get_total_discount(self, value):
        return value.students.aggregate(Sum("discount_amount"))["discount_amount__sum"]

class CalendarSerializer(serializers.ModelSerializer):

    room_name = serializers.CharField(source="room.name", read_only=True)
    class_name = serializers.CharField(source="_class.name", read_only=True)
    class_start_date = serializers.DateField(source="_class.start_date", read_only=True)
    class_end_date = serializers.DateField(source="_class.end_date", read_only=True)
    lesson_color = serializers.CharField(source="_class.lesson.color", read_only=True)

    class Meta:
        model = local_models.Calendar
        fields = "__all__"
        extra_kwargs = {
            "_class": { "required": False }
        }

    def validate(self, data):
        _class = data["_class"] if self.instance is None else self.instance._class
        if data["room"].branch.id != _class.branch.id:
            raise PermissionDenied
        if data["date"] > _class.end_date or data["date"] < _class.start_date:
            raise serializers.ValidationError("Day should be between 0 and 6")
        if data["end_time"] < data["start_time"]:
            raise serializers.ValidationError("End time should be later than the start time!")
        today_date = datetime.now()
        calendar = local_models.Calendar.objects.filter(
            room=data["room"].id,
            date=data["date"],
            start_time__lte=data["start_time"],
            end_time__gte=data["start_time"],
        )
        if self.instance is not None:
            calendar = calendar.exclude(id=self.instance.id)
        if calendar.exists():
            raise serializers.ValidationError("Room is occupied!")
        return data


class ExamUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Exam
        fields = "__all__"
        read_only_fields = [ "id", "_class" ]

    def validate_date(self, value):
        if value < datetime.date(datetime.now()):
            raise serializers.ValidationError("Start date should be later than the today's date!")
        return value


class ShortClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Class
        fields = [ "id", "name" ]


class ShortRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Room
        fields = [ "id", "name" ]


class ShortLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Lesson
        fields = [ "id", "name", "branch" ]


class LessonWithAnnotationSerializer(serializers.ModelSerializer):

    total = serializers.FloatField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    total_discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = local_models.Lesson
        fields = [ "id", "name", "branch", "total", "total_discount", "students_count", "price" ]

    def get_total_discount(self, value):
        return value.classes.aggregate(total=Sum("students__discount_amount"))["total"]

    def get_students_count(self, value):
        return value.classes.aggregate(count=Count("students"))["count"]

class TeacherProfileSerializer(serializers.Serializer):

    user = authapp_serializers.CustomUserSerializer()
    class_count = serializers.DictField()
    student_count = serializers.DictField()


class StaffProfileSerializer(serializers.Serializer):

    user = authapp_serializers.CustomUserSerializer()


class CalendarCreateSerializer(serializers.ModelSerializer):
    
    repeat = serializers.BooleanField(default=False)

    class Meta:
        model = local_models.Calendar
        field = "__all__"

