# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model 
User = get_user_model()

def list_datasheet(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        datasheets = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        datasheets = queryset.filter(
            branch__school=user.school, 
            **filter_queries
        )
    else:
        datasheets = queryset.filter(
            branch=user.branch,
            **filter_queries
        )
    return datasheets

def list_datasheet_status(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        datasheet_status = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        datasheet_status = queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        datasheet_status = queryset.filter(branch=user.branch)
    return datasheet_status
