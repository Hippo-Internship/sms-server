# Python imports
from functools import wraps
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


def object_exists(model, detail, many=False):
    def _object_exists(func):
        @wraps(func)
        def wrapper(self, request, pk=None, *args, **kwargs):
            _object = model.objects.filter(id=pk)
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