from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(email=email, password=password, username=username)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    profile = models.URLField(blank=True, null=True)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]
    object = UserManager()
