from django.urls import path
from .view import EventCreateGetListAPI, EventFormCreateGetAPI


urlpatterns = [
    path("", EventCreateGetListAPI.as_view()),
    path("<int:pk>/", EventCreateGetListAPI.as_view()),
    path("form/", EventFormCreateGetAPI.as_view()),
    path("form/<int:pk>/", EventFormCreateGetAPI.as_view()),
]
