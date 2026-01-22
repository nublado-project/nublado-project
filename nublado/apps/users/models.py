from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampModel, UUIDModel
from .managers import UserManager


class User(UUIDModel, TimestampModel, PermissionsMixin, AbstractBaseUser):
    username = models.CharField(
        verbose_name=_("label_username"),
        max_length=50,
        unique=True,
    )
    email = models.EmailField(
        verbose_name=_("label_email"),
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_("label_first_name"),
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name=_("label_last_name"),
        max_length=100,
    )
    is_active = models.BooleanField(verbose_name=_("label_is_active"), default=False)
    is_admin = models.BooleanField(verbose_name=_("label_is_admin"), default=False)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    def __str__(self):
        return "{0} : {1}".format(self.email, self.get_full_name())

    def clean(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
