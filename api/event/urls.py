from django.urls import path
from .view import EventCreateGetListAPI, EventFormCreateGetAPI, EventFormSubmitAPI


urlpatterns = [
    path("", EventCreateGetListAPI.as_view()),
    path("<int:pk>/", EventCreateGetListAPI.as_view()),
    path("form/", EventFormCreateGetAPI.as_view()),
    path("form/<int:pk>/", EventFormCreateGetAPI.as_view()),
    path("form/submit/", EventFormSubmitAPI.as_view()),
]
