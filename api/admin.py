from django.contrib import admin
from .models import User, Event


admin.site.register([User, Event])
# Register your models here.
