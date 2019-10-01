from apps.settings import SECRET_KEY, JWTOKEN_PREFIX
import jwt  # pip install pyjwt


def encode_jwtoken_key(payload):
    '''Generates a JSON Web Token with user info and expiry time.'''

    key = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return key.decode('utf-8')


def decode_jwtoken_key(key):
    '''Decodes from a JSON Web Token user info and expiry time.'''

    payload = jwt.decode(key, SECRET_KEY)
    return payload


def set_jwtoken_key_in_header(key):
    '''Sets a JSON Web Token header with prefix and key.'''

    header = JWTOKEN_PREFIX + ' ' + key
    return header


def get_jwtoken_key_from_header(header):
    '''Gets from a JSON Web Token header valid prefix and key.'''

    header = header.split()

    if header and len(header) == 2 and header[0] == JWTOKEN_PREFIX:
        return header[1]
    else:
        return None
