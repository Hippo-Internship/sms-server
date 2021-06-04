# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model 
User = get_user_model()

def list_groups(user, queryset, filter_queries={}):
    print(user.groups.role_id)
    groups_switch = {
        User.SUPER_ADMIN: {},
        User.ADMIN: {
            "role_id__gt": User.ADMIN,
        },
        User.OPERATOR: {
            "role_id__gt": User.OPERATOR
        },
    }
    return queryset.filter(**groups_switch[user.groups.role_id])

def list_users(user, queryset, filter_queries={}, groups=None):
    if groups is None:
        return []
    if user.groups.role_id > groups:
        raise PermissionDenied()
    if user.groups.role_id == User.SUPER_ADMIN:
        users = queryset.filter(groups__role_id=groups, is_active=True, **filter_queries)
    elif user.groups.role_id == User.ADMIN:
        users = user.school.users.filter(groups__role_id=groups, is_active=True, **filter_queries)
    elif user.groups.role_id == User.OPERATOR:
        users = user.branch.users.filter(groups__role_id=groups, is_active=True)
    else:
        return []
    return users