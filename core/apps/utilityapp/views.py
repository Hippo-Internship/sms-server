# Django built-in imports
from django.shortcuts import render
from django.contrib.auth.models import Group
# Third party imports
from rest_framework import \
        views, \
        viewsets
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        services as local_services 
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
from core.apps.schoolapp import \
        services as schoolapp_services, \
        serializers as schoolapp_serializers
from core.apps.datasheetapp import \
        services as datasheetapp_services, \
        serializers as datasheetapp_serializers

detail_with_filter = [ "user", "class", "room", "lesson", "discount", "status", "payment", "datasheet_status" ]

detail_switch = {
    "groups": {
        "service": authapp_services.list_groups,
        "params": {
            "queryset": Group.objects,
            "filter_queries": {}
        },
        "serializer": authapp_serializers.GroupsSerializer
    },
    "user": {
        "service": authapp_services.list_users,
        "params": {
            "queryset": authapp_serializers.User.objects,
            "groups": 0,
            "filter_queries": {}
        },
        "serializer": authapp_serializers.ShortUserSerializer
    },
    "class": {
        "service": classapp_services.list_classes,
        "params": {
            "queryset": classapp_serializers.local_models.Class.objects,
            "filter_queries": {}
        },
        "serializer": classapp_serializers.ShortClassSerializer
    },
    "room": {
        "service": classapp_services.list_rooms,
        "params": {
            "queryset": classapp_serializers.local_models.Room.objects,
            "filter_queries": {}
        },
        "serializer": classapp_serializers.ShortRoomSerializer
    },
    "lesson": {
        "service": classapp_services.list_lessons,
        "params": {
            "queryset": classapp_serializers.local_models.Lesson.objects,
            "filter_queries": {}
        },
        "serializer": classapp_serializers.ShortLessonSerializer
    },
    "discount": {
        "service": studentapp_services.list_discounts,
        "params": {
            "queryset": studentapp_serializers.local_models.Discount.objects,
            "filter_queries": {}
        },
        "serializer": studentapp_serializers.ShortDiscountSerializer
    },
    "status": {
        "service": local_services.list_status,
        "params": {
            "queryset": local_models.Status.objects,
            "filter_queries": {}
        },
        "serializer": local_serializers.ShortStatusSerializer
    },
    "payment": {
        "service": local_services.list_payment_methods,
        "params": {
            "queryset": local_models.PaymentMethod.objects,
            "filter_queries": {}
        },
        "serializer": local_serializers.ShortPaymentMethodSerializer
    },
    "school": {
        "service": schoolapp_services.list_school,
        "params": {
            "queryset": schoolapp_serializers.local_models.School.objects,
            "filter_queries": {}
        },
        "serializer": schoolapp_serializers.SchoolShortSerializer
    },
    "branch": {
        "service": schoolapp_services.list_branch,
        "params": {
            "queryset": schoolapp_serializers.local_models.Branch.objects,
            "filter_queries": {}
        },
        "serializer": schoolapp_serializers.BranchShortSerializer
    },
    "datasheet_status": {
        "service": datasheetapp_services.list_datasheet_status,
        "params": {
            "queryset": datasheetapp_serializers.local_models.Status.objects,
            "filter_queries": {}
        },
        "serializer": datasheetapp_serializers.ShortDatasheetStatuSerializer
    },
}


class StatusViewSet(viewsets.ModelViewSet):

    queryset = local_models.Status.objects.all()
    serializer_class = local_serializers.StatusSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.StatusGetOrModifySerializer,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        statuses = local_services.list_status(request_user, self.get_queryset())
        p_statuses = self.paginate_queryset(statuses)
        statuses = self.get_serializer_class()(p_statuses, many=True)
        return self.get_paginated_response(statuses.data)

    @core_decorators.object_exists(model=local_models.Status, detail="Status")
    def retrieve(self, request, status=None):
        data = super(StatusViewSet, self).retrieve(request, status.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(StatusViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.Status, detail="Status")
    def update(self, request, status=None):
        data = super(StatusViewSet, self).update(request, status.id).data
        return core_responses.request_success_with_data(data)


class PaymentMethodViewSet(viewsets.ModelViewSet):

    queryset = local_models.PaymentMethod.objects.all()
    serializer_class = local_serializers.PaymentMethodSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [ 
        core_permissions.PaymentMethodGetOrModifySerializer,
        core_permissions.BranchContentManagementPermission,
    ]

    def list(self, request):
        request_user = request.user
        pay_methods = local_services.list_payment_methods(request_user, self.get_queryset())
        p_pay_methods = self.paginate_queryset(pay_methods)
        pay_methods = self.get_serializer_class()(p_pay_methods, many=True)
        return self.get_paginated_response(pay_methods.data)

    @core_decorators.object_exists(model=local_models.PaymentMethod, detail="PaymentMethod")
    def retrieve(self, request, pay_method=None):
        data = super(StatusViewSet, self).retrieve(request, pay_method.id).data
        return core_responses.request_success_with_data(data)

    def create(self, request):
        data = super(StatusViewSet, self).create(request).data
        return core_responses.request_success_with_data(data)

    @core_decorators.object_exists(model=local_models.PaymentMethod, detail="PaymentMethod")
    def update(self, request, pay_method=None):
        data = super(StatusViewSet, self).update(request, pay_method.id).data
        return core_responses.request_success_with_data(data)


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
        school = request.data.get("school", 0)
        if school != 0 or type(school).__name__ != "int":
            detail_switch["branch"]["params"]["school"] = school
        else:
            detail_switch["branch"]["params"].pop("school", None)
        branch = request.data.get("branch", 0)
        filtered = False
        if branch != 0 or type(branch).__name__ != "int":
            filtered = True
            for item in projection:
                detail_switch[item]["params"]["filter_queries"]["branch"] = branch
        data = {}
        for key in projection:
            if key not in detail_switch:
                continue
            detail = detail_switch[key]
            data[key] = detail["serializer"](detail["service"](user=request_user, **detail["params"]), many=True).data
        if filtered:
            for item in projection:
                detail_switch[item]["params"]["filter_queries"].pop("branch", None)
        return core_responses.request_success_with_data(data)