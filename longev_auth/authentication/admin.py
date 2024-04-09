from django.contrib import admin

from .models import OtpCode


@admin.register(OtpCode)
class Users(admin.ModelAdmin):
    list_display = (
        "otp",
        "user",
        "exp_time",
    )
