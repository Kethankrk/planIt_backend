from django.urls import path
from .view import SignUpAPI, LoginAPI

urlpatterns = [
    path("signup/", SignUpAPI.as_view()),
    path("login/", LoginAPI.as_view()),
]
