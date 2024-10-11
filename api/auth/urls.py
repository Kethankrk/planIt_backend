from django.urls import path
from .view import SignUpAPI, LoginAPI, EmailVerificationAPI, GoogleAuthAPI

urlpatterns = [
    path("signup/", SignUpAPI.as_view()),
    path("google-auth/", GoogleAuthAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("email-verify/", EmailVerificationAPI.as_view()),
]
