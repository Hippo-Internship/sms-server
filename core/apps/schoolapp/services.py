# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model 
User = get_user_model()

def list_school(user, queryset, filter_queries={}):
    return queryset.all()

def list_branch(user, queryset, school=None, filter_queries={}):
    if "branch__school" in filter_queries:
        filter_queries["school"] = filter_queries.pop("branch__school")
    if school != None:
        filter_queries["school"] = school
    if user.groups.role_id is User.SUPER_ADMIN:
        branches = queryset.filter(**filter_queries) 
    elif user.groups.role_id is User.ADMIN:
        branches = queryset.filter(school=user.school)
    else:
        branches = []
    return branches