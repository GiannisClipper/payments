from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def core_exception_handler(exc, context):

    handlers = {
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'ValidationError': _handle_generic_error,
        'IntegrityError': _handle_generic_error,
    }

    response = exception_handler(exc, context)

    # Identify the type of the current exception and check
    # if it should be handled here or by the default handler

    print(exc.get_full_details())

    exception_class = exc.__class__.__name__

    if not response:
        if exception_class in ('ValidationError',):
            response = Response(exc.message_dict, status=status.HTTP_400_BAD_REQUEST)
            # print(exc.error_dict, exc.message_dict, exc.messages)

        elif exception_class in ('IntegrityError',):
            response = Response(exc.args[0], status=status.HTTP_400_BAD_REQUEST)
            # print(exc.args)

    if response and exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):

    # Wrap in `errors` key the response
    # generated by DRF or by project

    if 'detail' in response.data:
        data = {'errors': response.data['detail']}
    else:
        data = {'errors': response.data}
    response.data = data

    return response
