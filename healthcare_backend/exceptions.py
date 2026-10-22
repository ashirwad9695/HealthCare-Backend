from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework to format
    consistent and informative JSON error responses across all endpoints.
    """
    response = exception_handler(exc, context)

    if response is not None:
        message = "An error occurred while processing your request."
        
        # Extract a human-friendly message
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                message = str(response.data['detail'])
            elif len(response.data) > 0:
                first_key = next(iter(response.data))
                first_val = response.data[first_key]
                if isinstance(first_val, list) and len(first_val) > 0:
                    message = f"{first_key}: {first_val[0]}"
                else:
                    message = f"{first_key}: {first_val}"
        elif isinstance(response.data, list) and len(response.data) > 0:
            message = str(response.data[0])

        custom_data = {
            "success": False,
            "status_code": response.status_code,
            "message": message,
            "errors": response.data
        }
        response.data = custom_data

    return response
