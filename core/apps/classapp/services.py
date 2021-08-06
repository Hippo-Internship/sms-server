# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model 
User = get_user_model()

def list_classes(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        classes = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        classes = queryset.filter(
            branch__school=user.school.id, 
            **filter_queries
        )
    elif user.groups.role_id == User.OPERATOR or user.groups.role_id == User.ACCOUNTANT:
        classes = queryset.filter(
            branch=user.branch, 
            **filter_queries
        )
    elif user.groups.role_id == User.TEACHER:
        classes = user.classes.filter(**filter_queries)
    else:
        classes = []
    return classes

def list_rooms(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        rooms = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        filter_queries.pop("school", 0)
        rooms = queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        rooms = queryset.filter(branch=user.branch)
    return rooms

def list_lessons(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        lessons = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        filter_queries.pop("school", 0)
        lessons = queryset.filter(branch__school=user.school.id, **filter_queries)
    else:
        lessons = queryset.filter(branch=user.branch)
    return lessons
    
def list_curriculums(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        curriculums = queryset.filter(**filter_queries)
    elif user.groups.role_id == User.ADMIN:
        curriculums = queryset.filter(school=user.school.id, **filter_queries)
    elif user.groups.role_id == User.OPERATOR:
        curriculums = queryset.filter(school=user.school.id, shared=True, **filter_queries)
    elif user.groups.role_id == User.TEACHER:
        currculum_id_list = user.classes.values_list("lesson__curriculums", flat=True)
        curriculums = queryset.filter(id__in=currculum_id_list, shared=True, **filter_queries)
    return curriculums