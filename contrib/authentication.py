from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import BadSignature, SignatureExpired

from config import configuration as conf


DEFAULT_EXPIRY = 3153600000


def _generate_token(payload, expires_in=DEFAULT_EXPIRY):
    refresh_payload = payload.copy()
    refresh_payload['ref'] = True
    header = {'v': 1}

    """Creating the token object."""
    serializer = TimedJSONWebSignatureSerializer(secret_key=conf.SECRET_KEY, expires_in=expires_in)
    payload = serializer.dump_payload(header, payload).decode('utf-8')
    token = serializer.dumps(payload).decode('utf-8')
    _payload, header = serializer.loads(token, return_header=True)

    """Creating the refresh token object."""
    serializer = TimedJSONWebSignatureSerializer(secret_key=conf.SECRET_KEY, expires_in=expires_in * 3)
    refresh_payload = serializer.dump_payload(header, refresh_payload).decode('utf-8')
    refresh_token = serializer.dumps(refresh_payload).decode('utf-8')
    return {'token': token, "iat": header['iat'], "exp": header['exp'], 'refresh': refresh_token}


def generate_token(payload):
    return _generate_token(payload)


def _verify_token(token, expires_in=DEFAULT_EXPIRY, return_header=False):
    serializer = TimedJSONWebSignatureSerializer(secret_key=conf.SECRET_KEY, expires_in=expires_in)
    try:
        payload, header = serializer.loads(token, return_header=True)
        payload = serializer.load_payload(payload)
        if return_header:
            return payload, header
        return payload
    except (BadSignature, SignatureExpired, Exception) as e:
        print(e)
        return None


def verify_token(token):
    payload = _verify_token(token)
    if payload is None:
        return None
    if type(payload) != dict:
        return None
    try:
        if 'ref' in payload.keys():
            return None
    except Exception:
        return None

    return payload


class HTTPAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token_string = request.META.get('HTTP_AUTHORIZATION', "Not Found")
        token = token_string.split(" ")[1]
        payload = verify_token(token)

        if not token_string or payload is None:
            raise exceptions.AuthenticationFailed('Authentication required to access this resource')

        return payload, None

