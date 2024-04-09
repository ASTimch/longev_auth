from core.constants import Limits, Messages
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    """
    Custom User model.
    """

    email = models.EmailField(
        verbose_name="Email address",
        blank=False,
        null=False,
        unique=True,
        max_length=Limits.EMAIL_LENGTH,
        error_messages={
            "unique": Messages.EMAIL_ALREADY_EXISTS,
        },
        validators=(EmailValidator(),),
    )

    first_name = models.CharField(
        verbose_name="First name",
        max_length=Limits.FIRST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        verbose_name="Last name",
        max_length=Limits.LAST_NAME_LENGTH,
        blank=True,
        null=True,
    )

    password = models.CharField(
        max_length=255,
    )

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("id",)
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.id}:{self.email}"
