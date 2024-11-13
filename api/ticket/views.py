from rest_framework.views import APIView
from utils.response import CustomResponse
from . import serializers
from api.models import Ticket, Event


class CreateTicketViewAPI(APIView):

    def post(self, request, pk=None):
        serializer = serializers.TicketSerializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()

        event = Event.objects.filter(pk=pk).first()

        if not event:
            return CustomResponse(message="Event not found for given id").failure()

        serializer.save()

        return CustomResponse(message="Ticket created successfully").success(status=201)

    def get(self, request, pk=None):

        event = Event.objects.filter(pk=pk).prefetch_related("tickets").first()

        if not event:
            return CustomResponse(message="Event not found for given id").failure()

        tickets = event.tickets.all()

        return CustomResponse(
            response=serializers.TicketSerializer(tickets, many=True).data
        ).success()

    def patch(self, request, pk=None):

        serializer = serializers.TicketSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return CustomResponse(error=serializer.errors).failure()

        serializer.save()

        return CustomResponse(message="Successfully upadated").success(status=204)
