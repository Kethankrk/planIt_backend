from utils.response import CustomResponse
from utils.auth_utils import CustomAuthClass, JWT_utils
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializer import EventSerializer, EventFormSerializer
from django.shortcuts import get_object_or_404
from api.models import Event, EventForm
from django.http import Http404


class EventCreateGetListAPI(APIView):
    authentication_classes = [CustomAuthClass]

    def post(self, request: Request, pk=None):
        serializer = EventSerializer(
            data={**request.data, "organizer_id": request.user.id}
        )

        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()

        serializer.save()
        return CustomResponse(message="Event created successfully").success(status=201)

    def get(self, request: Request, pk=None):
        if pk is None:
            events = Event.objects.all()
            return CustomResponse(
                response=EventSerializer(events, many=True).data
            ).success()
        try:
            event = get_object_or_404(Event, pk=pk)
        except Http404:
            return CustomResponse(message="No event found for the given id").failure(
                status=404
            )
        return CustomResponse(response=EventSerializer(event).data).success()


class EventFormCreateGetAPI(APIView):

    def post(self, request: Request, pk=None):
        serializer = EventFormSerializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()

        serializer.save()

        return CustomResponse(message="Successfully created event form").success()

    def get(self, request: Request, pk=None):
        event: Event = (
            Event.objects.prefetch_related("forms__fields__options")
            .filter(pk=pk)
            .first()
        )
        if event is None:
            return CustomResponse(message="No event found with the given id").error()

        serializer = EventFormSerializer(event.forms)
        return CustomResponse(response=serializer.data).success()
