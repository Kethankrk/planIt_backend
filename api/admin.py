from django.contrib import admin
from .models import User, Event, EventForm, FormField, FieldOptions


admin.site.register([User, Event, EventForm, FormField, FieldOptions])
# Register your models here.
