from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled, AuthenticationFailed, NotAuthenticated


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):  # check that a Throttled exception is raised
        custom_response_data = {  # prepare custom response data
            'detail': f'Tu solicitud ha sido limitada. Por favor, intenta de nuevo en {exc.wait} segundos.',
            # 'availableIn': '%d seconds' % exc.wait
        }
        response.data = custom_response_data  # set the custom response data on response object

    if isinstance(exc, NotAuthenticated):
        response.data = {
            'code': 401,
            'message': 'Unauthorized'
        }

    return response
