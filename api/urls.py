from django.urls import path, include


urlpatterns = [
    path("auth/", include("api.auth.urls")),
    path("event/", include("api.event.urls")),
]
