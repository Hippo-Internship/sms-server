# Django built-in imports
from django.db.models.aggregates import Count
from django.db.models.fields import CharField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Sum, F
from rest_framework.exceptions import PermissionDenied
# Third party imports
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.settings import api_settings
# Local imports
from . import \
        models as local_models, \
        serializers as local_serializers, \
        services as local_services, \
        utils as local_utils
from core import \
        decorators as core_decorators, \
        permissions as core_permissions, \
        responses as core_responses, \
        utils as core_utils
from core.apps.classapp import serializers as classapp_serializers

# User Model
User = get_user_model()

user_search_filter_model = {
    "phone": "phone__startswith",
    "firstname": "firstname__startswith",
    "branch": "branch"
}

school_query_model = {
    "school": "school",
    "branch": "branch"
}

class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = local_serializers.CustomUserSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [
        core_permissions.UserGetOrModifyPermission,
        core_permissions.SchoolContentManagementPermission,
        core_permissions.BranchContentManagementPermission
    ]

    def list(self, request):
        query_params = core_utils.normalize_data(
            {
                "phone": "str",
                "firstname": "str",
                "branch": "int"
            },
            dict(request.query_params)
        )
        filter_queries = core_utils.build_filter_query(user_search_filter_model, query_params, user=request.user)
        filter_queries["groups__role_id"] = User.STUDENT
        users = local_services.list_users(request.user, self.get_queryset(), filter_queries=filter_queries)
        users = self.get_serializer_class()(users, many=True)
        return core_responses.request_success_with_data(users.data)

    @action(detail=True, methods=[ "GET" ])
    @core_decorators.object_exists(model=Group, detail="Group", field="role_id")
    def group(self, request, groups=None):
        request_user = request.user
        query_params = core_utils.normalize_data(
            { 
                "school": "int",
                "branch": "int"
            },
            dict(request.query_params)
        )
        filter_queries = core_utils.build_filter_query(school_query_model, query_params, user=request_user)
        filter_queries["groups__role_id"] = groups.role_id
        users = local_services.list_users(request_user, self.get_queryset(), filter_queries=filter_queries)
        if groups.role_id == User.TEACHER:
            users = users.annotate(job_hour=Sum(F("classes__calendar__end_time") - F("classes__calendar__start_time"), output_field=CharField())).order_by("-id")
        p_users = self.paginate_queryset(users)
        users = self.get_serializer_class()(p_users, many=True, context={ "request": request })
        return self.get_paginated_response(users.data)

    @core_decorators.object_exists(model=User, detail="User")
    def retrieve(self, request, user):
        generated_data = { "user": user }
        if user.groups.role_id == User.OPERATOR:
            generated_data = local_services.generate_operator_profile_data(user)
            serializer = local_serializers.OperatorProfileSerializer
        elif user.groups.role_id == User.TEACHER:
            generated_data = {
                "user": user,
                "class_count": local_services.generate_teacher_class_data(user),
                "student_count": local_services.generate_teacher_student_data(user)
            }
            serializer = classapp_serializers.TeacherProfileSerializer
        else:
            generated_data = user
            generated_data = {
                "user": user
            }
            # serializer = self.get_serializer_class()
            serializer = classapp_serializers.StaffProfileSerializer
        user = serializer(generated_data, context={ 'request': request })
        return core_responses.request_success_with_data(user.data)

    @action(detail=True, methods=[ "GET" ], url_path="profile")
    @core_decorators.object_exists(model=User, detail="User")
    def action_profile(self, request, user):
        generated_data = { "user": user }
        request_user = request.user
        request_user_role_id = request_user.groups.role_id
        if user.groups.role_id in User.FORBIDDEN_USER_ACCESS[request_user_role_id]:
            return core_responses.request_denied()
        if request_user_role_id == User.ADMIN:
            if request_user.school.id != user.school.id:
                return core_responses.request_denied()
        elif request_user_role_id != User.SUPER_ADMIN:
            if request_user.branch.id != user.branch.id:
                return core_responses.request_denied()
        if user.groups.role_id == User.OPERATOR:
            generated_data = local_services.generate_operator_profile_data(user)
            serializer = local_serializers.OperatorProfileSerializer
        elif user.groups.role_id == User.TEACHER:
            generated_data = {
                "user": user,
                "class_count": local_services.generate_teacher_class_data(user),
                "student_count": local_services.generate_teacher_student_data(user)
            }
            serializer = classapp_serializers.TeacherProfileSerializer
        else:
            generated_data = user
            generated_data = {
                "user": user
            }
            serializer = classapp_serializers.StaffProfileSerializer
        user = serializer(generated_data, context={ 'request': request })
        return core_responses.request_success_with_data(user.data)

    def create(self, request):
        user_request_data = request.data
        user = self.get_serializer_class()(data=user_request_data)
        user.is_valid(raise_exception=True)
        if not local_utils.can_user_manage(request.user.groups, user.validated_data["groups"]):
            raise PermissionDenied()
        user = user.save()
        profile = local_serializers.UserProfileSerializer(user.profile, data=user_request_data)
        profile.is_valid(raise_exception=True)
        profile.save()
        user = self.get_serializer_class()(user, many=False)
        return core_responses.request_success_with_data(user.data)

    @core_decorators.object_exists(model=User, detail="User")
    def destroy(self, request, user=None):
        if not local_utils.can_user_manage(request.user.groups, user.groups):
            raise PermissionDenied()
        user.is_active = False
        user.save()
        return core_responses.request_success()

    @core_decorators.object_exists(model=User, detail="User")
    def update(self, request, user=None):
        if not local_utils.can_user_manage(request.user.groups, user.groups, request.user, user):
            raise PermissionDenied()
        user_request_data = request.data.copy()
        upd_user = self.get_serializer_class()(user, data=user_request_data, user=request.user)
        upd_user.is_valid(raise_exception=True)
        user_request_data["user"] = user.id
        upd_profile = local_serializers.UserProfileSerializer(user.profile, data=user_request_data)
        upd_profile.is_valid(raise_exception=True)
        upd_profile.save()       
        upd_user.save()
        return core_responses.request_success_with_data(upd_user.data)
        
    def get_serializer_class(self):
        if self.action == "update":
            return local_serializers.CustomUserUpdateSerializer
        if self.action == "list":
            return local_serializers.ShortUserSerializer
        return super().get_serializer_class()