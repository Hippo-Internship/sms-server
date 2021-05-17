# Django built-in imports
from django.shortcuts import render
from django.contrib.auth.models import Group
# Third party imports
from rest_framework import \
        views, \
        viewsets, \
        decorators as rest_decorators
# Local imports
from core import \
        decorators as core_decorators, \
        responses as core_responses, \
        permissions as core_permissions
from core.apps.authapp import \
        services as authapp_services, \
        serializers as authapp_serializers
from core.apps.classapp import \
        services as classapp_services, \
        serializers as classapp_serializers
from core.apps.studentapp import \
        services as studentapp_services, \
        serializers as studentapp_serializers

detail_switch = {
    "groups": {
        "service": authapp_services.list_groups,
        "params": {
            "queryset": Group.objects,
        },
        "serializer": authapp_serializers.GroupsSerializer
    },
    "user": {
        "service": authapp_services.list_users,
        "params": {
            "queryset": authapp_serializers.User.objects,
            "groups": 0
        },
        "serializer": authapp_serializers.ShortUserSerializer
    },
    "class": {
        "service": classapp_services.list_classes,
        "params": {
            "queryset": classapp_serializers.local_models.Class.objects,
        },
        "serializer": classapp_serializers.ShortClassSerializer
    },
    "room": {
        "service": classapp_services.list_rooms,
        "params": {
            "queryset": classapp_serializers.local_models.Room.objects,
        },
        "serializer": classapp_serializers.ShortRoomSerializer
    },
    "lesson": {
        "service": classapp_services.list_lessons,
        "params": {
            "queryset": classapp_serializers.local_models.Lesson.objects,
        },
        "serializer": classapp_serializers.ShortLessonSerializer
    },
    "discount": {
        "service": studentapp_services.list_discounts,
        "params": {
            "queryset": studentapp_serializers.local_models.Discount.objects,
        },
        "serializer": studentapp_serializers.ShortDiscountSerializer
    }
}

class ListDetailView(views.APIView):

    @core_decorators.has_key("projection")
    def post(self, request, format=None):
        request_user = request.user
        projection = request.data["projection"]
        if type(projection).__name__ != "list":
            return core_responses.request_denied()
        if len(projection) > 5:
            return core_responses.request_denied()
        detail_switch["user"]["params"]["groups"] = request.data.get("groups", 0)
        data = {}
        for key in projection:
            if key not in detail_switch:
                continue
            detail = detail_switch[key]
            data[key] = detail["serializer"](detail["service"](user=request_user, **detail["params"]), many=True).data
        return core_responses.request_success_with_data(data)