# Django built-in imports
# Third party imports
from rest_framework.permissions import BasePermission
# Local imports


class UserGetOrModifyPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if view.action is "retrieve":
            return user.has_perm("authapp.view_customuser")
        else:
            return user.has_perms([
                "authapp.add_customuser",
                "authapp.delete_customuser",
                "authapp.change_customuser" 
            ])
