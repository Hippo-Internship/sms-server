# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError, NotFound
# Local imports
from core.apps.schoolapp import models as schoolapp_models


# User model
User = get_user_model()

def generate_basic_permission_switch(app_name, model_name):
    return {
        "list": app_name + ".view_" + model_name,
        "create": app_name + ".add_" + model_name,
        "update": app_name + ".change_" + model_name,
        "destroy": app_name + ".delete_" + model_name,
        "retrieve": app_name + ".view_" + model_name,
    }


class BranchContentManagementPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.groups.role_id == User.SUPER_ADMIN:
            return True

        if view.action == "create" or view.action == "update":
            request_data = request.data
            branch_id = request_data.get("branch", -1)
            branch = schoolapp_models.Branch.objects.filter(id=branch_id)
            if not branch.exists():
                raise NotFound({ "detail": "Branch does not exist!", "success": False })
            branch = branch[0]
            if user.groups.role_id == User.ADMIN:
                if branch.school.id is not user.school.id:
                    return False
                else:
                    return True
            if branch.id is not user.branch.id:
                return False
        elif view.action == "retrieve" or view.action == "destroy":
            _object = view.get_queryset().filter(id=view.kwargs["pk"])
            if not _object.exists():
                raise NotFound({ "detail": "Room does not exist!", "success": False })
            _object = _object[0]
            if user.groups.role_id == User.ADMIN:
                if _object.branch.school.id is not user.school.id:
                    return False
                else:
                    return True
            if _object.branch.id is not user.branch.id:
                return False
        return True


# class 


class UserGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        app_name = "authapp"
        model_name = "customuser"
        switch = generate_basic_permission_switch(app_name, model_name)
        switch["group"] = app_name + ".view_" + model_name
        return user.has_perm(switch.get(view.action, ""))


class SchoolGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("schoolapp", "school")
        return user.has_perm(switch.get(view.action, ""))


class BranchGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("schoolapp", "branch")
        return user.has_perm(switch.get(view.action, ""))


class LessonGetOrModifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "lesson")
        return user.has_perm(switch.get(view.action, ""))


class LessonGetOrModifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "lesson")
        return user.has_perm(switch.get(view.action, ""))


class RoomGetOrModifyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("classapp", "room")
        return user.has_perm(switch.get(view.action, ""))