from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, name):
        user = self.create_user(email=email, password=password, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    profile = models.URLField(blank=True, null=True)
    first_name = None
    last_name = None
    username = None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]
    object = UserManager()


class Event(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    hero_image = models.URLField()
    attendees_req = ArrayField(models.CharField(max_length=255))
    location = models.CharField(max_length=255)
    organizer_id = models.ForeignKey(
        User, related_name="organized_event", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title


class EventForm(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_id = models.OneToOneField(
        Event, related_name="forms", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.title


class FormField(models.Model):
    label = models.CharField(max_length=125)
    type = models.CharField(max_length=25)
    is_required = models.BooleanField(default=False)
    order_no = models.SmallIntegerField()
    form_id = models.ForeignKey(
        EventForm, related_name="fields", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.label


class FieldOptions(models.Model):
    option = models.CharField(max_length=125)
    field_id = models.ForeignKey(
        FormField, related_name="options", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.option


class FormResponse(models.Model):
    value = models.CharField(max_length=255)
    form_field = models.ForeignKey(
        FormField, related_name="values", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.form_field.label


class Ticket(models.Model):
    title = models.CharField(max_length=25)
    price = models.FloatField(null=True, blank=True)
    limit = models.IntegerField(null=True, blank=True)
    perks = ArrayField(models.CharField(max_length=255))
    event_id = models.ForeignKey(
        Event, related_name="tickets", on_delete=models.CASCADE
    )
