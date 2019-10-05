from rest_framework.renderers import JSONRenderer
import json


# class GenericJSONRenderer(JSONRenderer): 
class GenericJSONRenderer:
### I faced an uresolved problem: Renderer did'nt send the modified data shape
### to response. So at the moment I use this hand-made renderer to get result

    charset = 'utf-8'
    data_namespace = 'data'

    ### def render(self, data, media_type=None, renderer_context=None):
    def render(self, data):

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


class UserJSONRenderer(GenericJSONRenderer):
    data_namespace = 'user'
