from django.contrib.auth import get_user_model

from datetime import datetime

import jwt  # pip install pyjwt

from apps.settings import (
    SECRET_KEY,
    JWTOKEN_PREFIX,
    JWTOKEN_DURATION
)

from .constants import (
    TOKEN_KEY_NOT_VALID,
    TOKEN_USER_NOT_EXISTS,
    TOKEN_USER_NOT_ACTIVE,
    TOKEN_KEY_EXPIRED,
    TOKEN_HEADER_NOT_VALID,
    TOKEN_HEADER_PREFIX_NOT_VALID,
)


class JWToken:
    '''Extends User model to support JWtokens authentication.'''

    @property  # This decorator defines a dynamic property
    def token(self):
        '''Generates a JSON Web Token with user info and expiry time.'''

        now = datetime.timestamp(datetime.utcnow())
        expiration = now + JWTOKEN_DURATION
        key = JWToken.encode_token_key({
            'user_id': self.pk,
            'expiration': expiration
        })

        return key

    def compose_token_header(key):
        '''Composes a JSON Web Token header with prefix and key.'''

        header = JWTOKEN_PREFIX + ' ' + key
        return header

    def decompose_token_header(header):
        '''Decomposes a valid JSON Web Token header and returns the key.'''

        header = header.split()

        if not header or len(header) != 2:
            raise Exception(TOKEN_HEADER_NOT_VALID)

        prefix = header[0].decode('utf-8')  # Convert binary to str
        key = header[1].decode('utf-8')  # Convert binary to str

        if prefix.lower() != JWTOKEN_PREFIX.lower():
            raise Exception(TOKEN_HEADER_PREFIX_NOT_VALID)

        return key

    def encode_token_key(payload):
        '''Generates a JSON Web Token with user info and expiry time.'''

        key = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return key.decode('utf-8')

    def decode_token_key(key):
        '''Decodes from a JSON Web Token user info and expiry time.'''

        try:
            payload = jwt.decode(key, SECRET_KEY)
        except Exception as err:
            raise Exception(TOKEN_KEY_NOT_VALID + ' ' + str(err))

        return payload

    def check_if_user_in_token_exists(id):
        '''Checks if the user's id in token exists in database.'''

        user = get_user_model().objects.get(pk=id)

        if not user:
            raise Exception(TOKEN_USER_NOT_EXISTS)

        return user

    def check_if_user_in_token_is_active(user):
        '''Checks if the user in token is active.'''

        if not user.is_active:
            raise Exception(TOKEN_USER_NOT_ACTIVE)

        return user

    def check_if_token_is_expired(expiration):
        '''Checks if the token is expired.'''

        now = datetime.timestamp(datetime.utcnow())

        if expiration <= now:
            raise Exception(TOKEN_KEY_EXPIRED)

        return expiration
