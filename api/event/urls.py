from django.urls import path
from .view import EventCreateGetListAPI


urlpatterns = [
    path("", EventCreateGetListAPI.as_view()),
    path("<int:pk>/", EventCreateGetListAPI.as_view()),
]
