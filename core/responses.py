# Third party imports
from rest_framework.response import Response
from rest_framework import status

def request_denied(*args, **kwargs):
    return Response(
        { "detail": "Request Denied!", "success": False }, 
        status=status.HTTP_400_BAD_REQUEST,
        *args, **kwargs
    )

def request_success_with_data(data, *args, **kwargs):
    return Response(
        { "data": data, "success": True },
        status=status.HTTP_200_OK,
        *args, **kwargs
    )

def request_success(*args, **kwargs):
    return Response(
        { "success": True },
        status=status.HTTP_200_OK,
        *args, **kwargs
    )