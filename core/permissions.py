# Django built-in imports
# Third party imports
from rest_framework.permissions import BasePermission
# Local imports


def generate_basic_permission_switch(app_name, model_name):
    return {
        "list": app_name + ".view_" + model_name,
        "create": app_name + ".add_b" + model_name,
        "update": app_name + ".chang" + model_name,
        "delete": app_name + ".delet" + model_name,
        "retrieve": app_name + ".view_" + model_name,
    }


class UserGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("authapp", "customuser")
        return switch[view.action]


class SchoolGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("schoolapp", "school")
        return switch[view.action]


class BranchGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        switch = generate_basic_permission_switch("schoolapp", "branch")
        return switch[view.action]