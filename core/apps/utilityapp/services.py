# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model
User = get_user_model()

def list_status(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        rooms = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        filter_queries.pop("branch__school", None)
        rooms = queryset.filter(branch__school=user.school.id, **filter_queries)
    elif user.groups.role_id == User.OPERATOR:
        rooms = queryset.filter(branch=user.branch)
    else:
        rooms = []
    return rooms


def list_payment_methods(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        rooms = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        filter_queries.pop("branch__school", None)
        rooms = queryset.filter(branch__school=user.school.id, **filter_queries)
    elif user.groups.role_id == User.OPERATOR:
        rooms = queryset.filter(branch=user.branch)
    else:
        rooms = []
    return rooms