from rest_framework.renderers import JSONRenderer

import json


class GenericJSONRenderer(JSONRenderer):

    charset = 'utf-8'
    data_namespace = 'data'

    def render(self, data, media_type=None, renderer_context=None):

        # If errors has been thrown, dict has an `errors` key
        errors = data.pop('errors', None)

        # If data is list, dict has an `objects` key
        objects = data.pop('objects', None)

        # If `token` key exists
        token = data.pop('token', None)

        # If `token` key is a byte object, needs to be decoded
        if token and isinstance(token, bytes):
            token = token.decode('utf-8')

        # Resend the `token` key included in request, except
        # a new one has been generated (whenever signing in)
        if token == None and renderer_context['request'].auth:
            token = renderer_context['request'].auth

            # TokenAuthentication provides on success following credentials:
            # request.user: a Django User instance
            # request.auth: a rest_framework.authtoken.models.Token instance

        data_ = data.copy()
        data.clear()

        if errors:
            data['errors'] = errors

        elif isinstance(objects, list):  # Including empty lists
            data[self.data_namespace] = objects

        else:
            data[self.data_namespace] = data_

        data['token'] = token  # Render `token` key out of data

        return json.dumps(data)
