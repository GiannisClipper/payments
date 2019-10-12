from rest_framework import authentication

from django.contrib.auth import get_user_model


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        request.user = None

        auth_header = authentication.get_authorization_header(request)

        if not auth_header:
            return None

        token = get_user_model().decompose_token_header(auth_header)

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):

        payload = get_user_model().decode_token_key(token)

        user_id, expiration = payload.values()

        user = get_user_model().check_if_user_in_token_exists(user_id)

        get_user_model().check_if_user_in_token_is_active(user)

        get_user_model().check_if_token_is_expired(expiration)

        return (user, token)
