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
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        validators=[UnicodeUsernameValidator(), MinLengthValidator(2)],
    )

    email = models.EmailField(
        verbose_name="Email address", blank=False, null=False, unique=True
    )

    first_name = models.CharField(
        verbose_name="First name", max_length=150, blank=True, null=True
    )

    last_name = models.CharField(
        verbose_name="Last name", max_length=150, blank=True, null=True
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
