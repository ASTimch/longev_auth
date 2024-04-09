from core.constants import Limits
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    """
    Custom User model.
    """

    username = models.CharField(
        verbose_name="User name",
        help_text="Please enter your unique username",
        max_length=Limits.USERNAME_LENGTH,
        blank=False,
        null=False,
        unique=True,
        validators=[UnicodeUsernameValidator(), MinLengthValidator(2)],
        error_messages={
            "unique": "This email already in use",
        },
    )

    email = models.EmailField(
        verbose_name="Email address",
        blank=False,
        null=False,
        unique=True,
        max_length=Limits.EMAIL_LENGTH,
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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("id",)
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.id}:{self.username}"
