from rest_framework.views import exception_handler

from .renderers import GenericJSONRenderer


def core_exception_handler(exc, context):

    handlers = {
        'ValidationError': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'Http404': _handle_generic_error,
    }

    response = exception_handler(exc, context)

    # Identify the type of the current exception and check
    # if it should be handled here or by the default handler

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):

    # Wrap in `errors` key the response
    # generated by DRF or by project

    if 'detail' in response.data:
        data = {'errors': response.data['detail']}
    else:
        data = {'errors': response.data}

    #rendered_data = GenericJSONRenderer().render(
    #    data, renderer_context=context
    #)

    #response.data = rendered_data
    response.data = data

    return response