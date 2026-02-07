from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

def success_response(data=None, message="Success", status_code=200):
    return Response({
        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }, status=status_code)

def error_response(message="Error", errors=None, status_code=400):
    return Response({
        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }, status=status_code)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "success": False,
            "message": "Something went wrong",
            "errors": response.data
        }, status=response.status_code)

    return Response({
        "success": False,
        "message": "Internal server error"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
