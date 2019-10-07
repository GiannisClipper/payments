from rest_framework import authentication

from .handlers import JWTokenHandler


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request)

        if not auth_header:
            return None

        token = JWTokenHandler.decompose_header(auth_header)

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        payload = JWTokenHandler.decode_key(token)

        user = JWTokenHandler.check_if_user_in_key_exists(payload['user_id'])

        JWTokenHandler.check_if_user_in_key_is_active(user)

        JWTokenHandler.check_if_key_is_expired(payload['expiration'])

        return (user, token)
