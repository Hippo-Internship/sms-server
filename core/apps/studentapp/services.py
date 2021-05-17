# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model
User = get_user_model()

def list_discounts(user, queryset, filter_queries={}):
    if user.groups.role_id == User.SUPER_ADMIN:
        discounts = queryset.all()
    elif user.groups.role_id == User.ADMIN:
        branches = user.school.branches.all()
        discounts = queryset.filter(branch__in=branches)
    elif user.groups.role_id == User.OPERATOR:
        discounts = queryset.filter(branch=user.branch)
    else:
        discounts = []
    return discounts

# def list_payments(user, queryset, filter_queries={}):
#     if user.groups.role_id == User.SUPER_ADMIN:
#         discounts = queryset.all()
#     elif user.groups.role_id == User.ADMIN:
#         branches = user.school.branches.all()
#         discounts = queryset.filter(branch__in=branches)
#     elif user.groups.role_id == User.OPERATOR:
#         discounts = queryset.filter(branch=user.branch)
#     else:
#         discounts = []
#     return discounts