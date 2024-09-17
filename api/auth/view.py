from rest_framework.views import APIView, Response
from .serializer import UserSerializer, LoginSerializer
from api.models import User
from utils.auth_utils import JWT_utils
from utils.response import CustomResponse


class SignUpAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()
        serializer.save()
        return CustomResponse(message="Successfully registered").success()


class LoginAPI(APIView):

    def post(self, request):
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
