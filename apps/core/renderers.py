# ### from rest_framework.renderers import JSONRenderer
# ### I faced a strange problem with JSONRenderer: Could'nt send the modified
# ### data dict to response. Temporarily I use a custom renderer to get result

import json


# ### class GenericJSONRenderer(JSONRenderer):
class GenericJSONRenderer:

    charset = 'utf-8'
    data_namespace = 'data'

    # ### def render(self, data, media_type=None, renderer_context=None):
    def render(self, data, renderer_context=None):

        token = None

        # When `data` is not a list but a single object,
        # lookup for `errors` or `token` key (new token)
        if not isinstance(data, list):

            # Whenever errors has been thrown,
            # `data` contains an `errors` key
            errors = data.get('errors', None)
            if errors:
                self.data_namespace = 'errors'
                data = data['errors']

            else:
                # If `token` key exists will be a byte object,
                # so we need to decode it to be serialized properly
                token = data.pop('token', None)
                if token and isinstance(token, bytes):
                    token = token.decode('utf-8')

        # New token generated while user signin, in other
        # cases resend the one that included in request
        if not token and renderer_context['request'].auth:
            token = renderer_context['request'].auth

            # TokenAuthentication provides on success following credentials:
            # request.user: a Django User instance
            # request.auth: a rest_framework.authtoken.models.Token instance

        # Render (`data` or `errors`) and `token` seperated
        return json.dumps({
            self.data_namespace: data,
            'token': token
        })


from rest_framework.renderers import JSONRenderer


class Generic2JSONRenderer(JSONRenderer):

    charset = 'utf-8'
    data_namespace = 'data'

    def render(self, data, media_type=None, renderer_context=None):

        errors = None
        token = None

        # When `data` is not a list but a single object,
        # lookup for `errors` or `token` key (new token)
        if not isinstance(data, list):

            # Whenever errors has been thrown,
            # `data` contains an `errors` key
            errors = data.pop('errors', None)

            # If `token` key exists will be a byte object,
            # so we need to decode it to be serialized properly
            token = data.pop('token', None)
            if token and isinstance(token, bytes):
                token = token.decode('utf-8')

        # New token generated while user signin, in other
        # cases resend the one that included in request
        if not token and renderer_context['request'].auth:
            token = renderer_context['request'].auth

            # TokenAuthentication provides on success following credentials:
            # request.user: a Django User instance
            # request.auth: a rest_framework.authtoken.models.Token instance

        data_ = data.copy()
        data.clear()

        # Render `data-or-errors` key and `token` key seperated
        if not errors:
            data[self.data_namespace] = data_
        else:
            data['errors'] = errors

        data['token'] = token

        return data
