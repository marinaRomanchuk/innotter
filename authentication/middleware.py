import json
import jwt
from django.http import HttpResponse
from django.conf import settings
from rest_framework import authentication

from user.models import User


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_request(request)

    def process_request(self, request):
        jwt_token = authentication.get_authorization_header(request)
        auth_header_prefix = "token"

        if jwt_token:
            try:
                jwt_token = jwt_token.split()
                if len(jwt_token) != 2:
                    return HttpResponse(json.dumps({"data": "Invalid number of arguments"}), status=401)

                if jwt_token[0].decode("utf-8").lower() != auth_header_prefix:
                    return HttpResponse(json.dumps({"data": "Invalid authentication prefix"}), status=401)

                payload = jwt.decode(jwt_token[1], settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload["user_id"]
                request.user = User.objects.get(id=user_id)

                return self.get_response(request)
            except jwt.ExpiredSignatureError:
                return HttpResponse(json.dumps({"data": "Authentication token has expired"}), status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                return HttpResponse(json.dumps({"data": "Authorization has failed, Please send valid token"}),
                                    status=401)

        return self.get_response(request)
