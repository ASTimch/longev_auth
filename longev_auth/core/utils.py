import base64
import os
from datetime import datetime

import pyotp
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


def get_user_token(user):
    token = RefreshToken.for_user(user)
    return {
        "token": str(token.access_token),
    }


def generate_otp_code():
    totp = pyotp.TOTP(
        base64.b32encode(os.urandom(16)).decode(),
        digits=settings.OTP_LENGTH,
    )
    otp = totp.now()
    return otp


def is_valid_user_otp(user, otp: str) -> bool:
    try:
        user_otp = user.otp
        if user_otp.otp != otp:
            return False
        print("otp.exp_time ", user_otp.exp_time, "now", timezone.now())
        if user_otp.exp_time < timezone.now():
            return False
        return True
    except ObjectDoesNotExist:
        return False
