from django.urls import path
from .view import SignUpAPI, LoginAPI, EmailVerificationAPI

urlpatterns = [
    path("signup/", SignUpAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("email-verify/", EmailVerificationAPI.as_view()),
]
