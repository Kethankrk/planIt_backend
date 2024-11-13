from rest_framework import serializers
from api.models import Event, EventForm, FormField, FieldOptions, FormResponse
from django.db import transaction


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"


class FieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOptions
        fields = ["option"]


class FormFieldSerializer(serializers.ModelSerializer):
    options = serializers.ListSerializer(
        child=serializers.CharField(), required=False, source="options__option"
    )

    class Meta:
        model = FormField
        fields = "__all__"
        read_only_fields = ["form_id"]

    def to_representation(self, instance: FormField):
        options = [option.option for option in instance.options.all()]
        representation = super().to_representation(instance)
        representation["options"] = options
        return representation


class EventFormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = EventForm
        fields = ["title", "description", "event_id", "fields"]

    def create(self, validated_data: dict):
        fields_data: list[dict] = validated_data.pop("fields", [])

        with transaction.atomic():
            event_form = EventForm.objects.create(**validated_data)

            for field in fields_data:
                options_data = field.pop("options", [])

                form_field = FormField.objects.create(form_id=event_form, **field)

                for option in options_data:
                    FieldOptions.objects.create(field_id=form_field, option=option)

        return event_form


class FormResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormResponse
        fields = "__all__"
