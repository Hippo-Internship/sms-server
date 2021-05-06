# Django built-in imports
# Third party imports
from rest_framework.permissions import BasePermission
# Local imports


class UserGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if view.action is "retrieve":
            return user.has_perm("authapp.view_customuser")
        elif view.action is "update":
            return user.has_perm("authapp.change_customuser")
        else:
            return user.has_perms([
                "authapp.add_customuser",
                "authapp.delete_customuser",
            ])


class SchoolGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if view.action is "retrieve":
            return user.has_perm("schoolapp.view_school")
        else:
            return user.has_perms([
                "schoolapp.add_school",
                "schoolapp.delete_school",
                "schoolapp.change_school",
            ])