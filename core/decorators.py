from functools import wraps
from rest_framework.response import Response

def has_key(key):
    def _has_key(func):
        @wraps(func)
        def wrapper(self, request, pk=None, *args, **kwargs):
            if key in request.data:
                return func(self, request, pk, *args, **kwargs)
            else:
                return Response({ "detail": key + " is not given!", "success": False }, status=400)

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
                return Response({ "detail": detail + " does not exist!", "success": False }, status=404)
        return wrapper
    return _object_exists