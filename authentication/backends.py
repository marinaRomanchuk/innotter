import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from user.models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = "token"

        if not auth_header:
            return None
        if len(auth_header) == 1 or len(auth_header) > 2:
            raise exceptions.AuthenticationFailed("Authorization failed, invalid number of arguments.")

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Authentication token has expired")
        except (jwt.DecodeError, jwt.InvalidTokenError):
            raise exceptions.AuthenticationFailed("Authorization failed, Please send valid token")

        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Authorization failed, user not found.")

        return user, token
