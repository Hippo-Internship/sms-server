# Python imports
from functools import wraps
from django.db.models import fields
# Third party imports
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

def has_key(key):
    def _has_key(func):
        @wraps(func)
        def wrapper(self, request, pk=None, *args, **kwargs):
            if key in request.data:
                return func(self, request, pk, *args, **kwargs)
            else:
                raise ValidationError({ "detail": key + " is not given!", "success": False })

        return wrapper
    return _has_key

def has_keys(*args):
    def _has_key(func):
        @wraps(func)
        def wrapper(self, request, pk=None, *args, **kwargs):
            for key in args:
                if key not in request.data:
                    raise ValidationError({ "detail": key + " is not given!", "success": False })
            return func(self, request, pk, *args, **kwargs)
        return wrapper
    return _has_key

def object_exists(model, detail, many=False, field=None):
    def _object_exists(func):
        @wraps(func)
        def wrapper(self, request, pk=None, *args, **kwargs):
            if field is None:
                _object = model.objects.filter(id=pk)
            else:
                _object = model.objects.filter(**{ field: pk })
            if _object.exists():
                return func(self, request, _object if many else _object[0], *args, **kwargs)
            else:
                raise NotFound({ "detail": detail + " does not exist!", "success": False })
        return wrapper
    return _object_exists


def testing(func):
    def wrapper(*args, **kwargs):
        print("dwq")
        func(*args, **kwargs)
    
    return wrapper