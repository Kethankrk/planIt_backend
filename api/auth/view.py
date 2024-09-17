from rest_framework.views import APIView, Response
from .serializer import UserSerializer, LoginSerializer, EmailVerificationSerializer
from api.models import User
from utils.auth_utils import JWT_utils
from utils.response import CustomResponse
from rest_framework.request import Request
from random import randint
from django.core.cache import cache
from django.core.mail import send_mail
from decouple import config


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

        if not user.check_password(password) and user.has_usable_password():
            return CustomResponse(message="Bad cridentails").failure()

        if not user.is_verified:
            return CustomResponse(message="User email is not verified").failure(
                status=403
            )
        token = JWT_utils.generate_token({"id": user.id})
        return CustomResponse(response={"token": token}).success()


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
