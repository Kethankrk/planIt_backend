from rest_framework.views import APIView, Response
from .serializer import (
    UserSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
    GoogleUserInfoSerailzier,
)
from api.models import User
from utils.auth_utils import JWT_utils
from utils.response import CustomResponse
from rest_framework.request import Request
from random import randint
from django.core.cache import cache
from django.core.mail import send_mail
from decouple import config
import requests


class SignUpAPI(APIView):
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()
        serializer.save()
        return CustomResponse(message="Successfully registered").success()


class LoginAPI(APIView):

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = User.object.filter(email=email).first()

        if user is None:
            return CustomResponse(message="User not found").failure()

        if not user.check_password(password):
            return CustomResponse(message="Bad cridentails").failure()

        if not user.is_verified:
            return CustomResponse(message="User email is not verified").failure(
                status=403
            )
        token = JWT_utils.generate_token({"id": user.id})
        return CustomResponse(response={"token": token}).success()


class GoogleAuthAPI(APIView):
    def post(self, request: Request):
        token = request.data.get("token")
        if token is None:
            return CustomResponse(message="Token not provided").failure()
        print(token)
        try:
            res = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )

            if res.status_code == 200:
                serializer = GoogleUserInfoSerailzier(res.json())

                email = serializer.data.get("email")
                user = User.object.filter(email=email).first()
                if not user is None:
                    jwt_token = JWT_utils.generate_token({"id": user.id})
                    return CustomResponse(response={"token": jwt_token}).success()

                user_serializer = UserSerializer(
                    data={**serializer.data, "is_verified": True}
                )
                if not user_serializer.is_valid():
                    print(user_serializer.errors)
                    return CustomResponse(error=user_serializer.errors).failure(
                        status=500
                    )
                user = user_serializer.save()
                jwt_token = JWT_utils.generate_token({"id": user.id})
                return CustomResponse(response={"token": jwt_token}).success()
            raise ValueError()
        except ValueError:
            return CustomResponse(message="Invalid token").failure()


class EmailVerificationAPI(APIView):

    def get(self, request: Request):
        email = request.query_params.get("email")
        if email is None:
            return CustomResponse(message="Email must be passed as params").failure()

        is_already_send = cache.get(email)

        if not is_already_send is None:
            return CustomResponse(message="Verification code already send.").failure()

        random_no = randint(1000, 9999)
        print(random_no)

        subject = "PlanIt email verification code"
        message = (
            f"The verification code is: {random_no}, this will be valid for 10 min."
        )
        from_email = config("GOOGLE_USER")
        recipient_list = [email]

        try:
            cache.set(email, random_no, timeout=600)
            send_mail(subject, message, from_email, recipient_list)
            return CustomResponse(message="Verification code send").success()
        except Exception as e:
            CustomResponse(message=str(e)).failure(status=500)

    def post(self, request: Response):

        serializer = EmailVerificationSerializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()

        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")

        stored_code = cache.get(email)

        if stored_code is None:
            return CustomResponse(message="Code expired").failure(status=403)

        if code != stored_code:
            return CustomResponse(message="Invalid code").failure(status=403)

        cache.delete(email)

        user: User = User.object.get(email=email)

        if user is None:
            return CustomResponse(message="User not found").failure(404)

        user.is_verified = True
        user.save()
        token = JWT_utils.generate_token({"id": user.id})
        return CustomResponse(
            message="Verification success", response={"token": token}
        ).success()
