from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class OtpCode(models.Model):
    """Otp codes for users."""

    otp = models.CharField(
        verbose_name="OTP code",
        help_text="OTP code",
        max_length=50,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="otp",
        verbose_name="User",
        unique=True,
        primary_key=True,
    )
    exp_time = models.DateTimeField(verbose_name="Expiration time")

    class Meta:
        verbose_name = "OTP code"
        verbose_name_plural = "Otp codes"

    def __str__(self):
        return f"{self.pk}: {self.otp}"
