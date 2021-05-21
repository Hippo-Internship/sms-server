# Django built-in imports
from django.contrib.auth import get_user_model
# Third party imports
from rest_framework.exceptions import PermissionDenied
# Local imports

# User model 
User = get_user_model()

def list_school(user, queryset, filter_queries={}):
    return queryset.all()