from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if not response:  # an unhandled error has caused empty response
        # todo: log error details
        response = Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={'detail': 'Oops! Server Side Error :/'}
        )

    return response
