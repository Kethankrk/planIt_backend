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
    title = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    hero_image = models.URLField()
    attendees_req = ArrayField(models.CharField(max_length=255))
    location = models.CharField(max_length=255)
    organizer_id = models.ForeignKey(
        User, related_name="organized_event", on_delete=models.SET_NULL, null=True
    )
