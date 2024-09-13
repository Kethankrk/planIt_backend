from rest_framework.views import APIView, Response
from .serializer import UserSerializer, LoginSerializer
from api.models import User
from utils.auth_utils import JWT_utils, CustomPermission


class SignUpAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response("success")


class LoginAPI(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = User.object.filter(email=email).first()

        if user is None:
            return Response("User not found", status=404)

        if not user.has_usable_password():
            token = JWT_utils.generate_token({"id": user.id})
            return Response({"token": token})

        if not user.check_password(password):
            return Response("Bad cridentails", status=401)

        token = JWT_utils.generate_token({"id": user.id})
        return Response({"access_token": token})
