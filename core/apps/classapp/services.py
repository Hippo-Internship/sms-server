# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model 
User = get_user_model()

def list_classes(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        classes = queryset.all()
    elif user.groups.role_id == User.ADMIN:
        classes = queryset.filter(
            branch__school=user.school.id, 
            **filter_queries
        )
    elif user.groups.role_id == User.OPERATOR:
        classes = queryset.filter(
            branch=user.branch, 
            **filter_queries
        )
    elif user.groups.role_id == User.TEACHER:
        classes = queryset.filter(
            teacher=user, 
            **filter_queries
        )
    else:
        classes = []
    return classes

def list_rooms(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        rooms = queryset.all()
    elif user.groups.role_id == User.ADMIN:
        branches = user.school.branches.all()
        rooms = queryset.filter(branch__in=branches)
    elif user.groups.role_id == User.OPERATOR:
        rooms = queryset.filter(branch=user.branch)
    else:
        rooms = []
    return rooms

def list_lessons(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        lessons = queryset.all()
    elif user.groups.role_id == User.ADMIN:
        branches = user.school.branches.all()
        lessons = queryset.filter(branch__in=branches)
    elif user.groups.role_id == User.OPERATOR:
        lessons = queryset.filter(branch=user.branch)
    else:
        lessons = []
    return lessons