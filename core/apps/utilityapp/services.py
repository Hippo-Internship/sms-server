# Django built-in imports
from django.db.models import Q
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model
User = get_user_model()

def list_status(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        status = queryset.filter(Q(default=True) | Q(**filter_queries))
    elif user.groups.role_id == User.ADMIN:
        status = queryset.filter(Q(default=True) | Q(branch__school=user.school.id, **filter_queries))
    else:
        status = queryset.filter(Q(default=True) | Q(branch=user.branch))
    return status


def list_payment_methods(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        payment_method = queryset.filter(Q(default=True) | Q(**filter_queries))
    elif user.groups.role_id == User.ADMIN:
        payment_method = queryset.filter(Q(default=True) | Q(branch__school=user.school.id, **filter_queries))
    else:
        payment_method = queryset.filter(Q(default=True) | Q(branch=user.branch))
    return payment_method