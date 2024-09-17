import jwt
from typing import Tuple
from decouple import config
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import BasePermission
from .exceptions import UnautherizedError, UserNotVerifiedError


class CustomPermission(BasePermission):
    def authenticate(self, request):
        JWT_utils.is_jwt_authenticated(request=request)


class JWT_utils:
    @staticmethod
    def generate_token(data: dict) -> Tuple[str, str]:
        secret = config("SECRET")
        return jwt.encode(data, secret, algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> dict:
        secret = config("SECRET")
        return jwt.decode(token, secret, algorithms=["HS256"])

    @staticmethod
    def get_user_id(request) -> str:
        token = get_authorization_header(request=request).decode("utf-8").split()
        payload = JWT_utils.decode_token(token=token[1])
        return payload["id"]

    @staticmethod
    def is_jwt_authenticated(request) -> dict:
        try:
            token = get_authorization_header(request).decode("utf-8")
            if not token or not token.startswith("Bearer"):
                raise UnautherizedError("Invalid token header")
            token = token.split()[1]
            payload = JWT_utils.decode_token(token)
        except IndexError as e:
            raise UnautherizedError("Empty token found")
        except jwt.exceptions.InvalidSignatureError as e:
            raise UnautherizedError("Invalid token")
        except Exception as e:
            raise UnautherizedError(str(e))
