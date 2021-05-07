# Python imports
from datetime import datetime
# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
# Local imports
from . import models as local_models
from core.apps.schoolapp import serializers as schoolapp_serializers

# User model
User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Lesson
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = local_models.Room
        fields = "__all__"


class ClassCreateAndUpdateSerializer(serializers.ModelSerializer):

    days = serializers.ListField(required=True)

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
            raise ValidationError("Such lesson does't exist in the branch!")
        return value

    def validate_teacher(self, value):
        if value.groups.role_id != User.TEACHER:
            raise ValidationError("Invalid teacher!")
        if value.branch.id != self.initial_data.get("branch", 0):
            raise ValidationError("Such lesson does't exist in the branch!")
        return value

    def room(self, value):
        if value.branch.id != self.initial_data.get("branch", 0):
            raise ValidationError("Such room does't exist in the branch!")
        return value

    def validate_days(self, value):
        if len(value) != 7:
            raise ValidationError("Days should contain only 7 elements!")
        return value

    def validate_start_date(self, value):
        initial_data = self.initial_data
        start_date = initial_data.get("start_date", None)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if start_date < datetime.now():
            raise ValidationError("Start date should be later than the today's date!")
        return value

    def validate_end_date(self, value):
        initial_data = self.initial_data
        start_date = initial_data.get("start_date", None)
        end_date = initial_data.get("end_date", None)
        if end_date < start_date:
            raise ValidationError("End date should be later than the start date!")
        return value

    def validate_end_time(self, value):
        initial_data = self.initial_data
        start_time = initial_data.get("start_time", None)
        end_time = initial_data.get("end_time", None)
        if start_time < end_time:
            raise ValidationError("End time should be later than the start time!")
        return value


class ClassDetailSerializer(serializers.ModelSerializer):

    branch = serializers.CharField(source="branch.name", read_only=True)
    teacher = serializers.CharField(source="teacher.name", read_only=True)
    lesson = serializers.CharField(source="lesson.name", read_only=True)
    room = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = local_models.Class
        fields = "__all__"
