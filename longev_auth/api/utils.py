import base64
import os

import pyotp
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .tasks import send_email
from core.constants import Messages


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
    return totp.now()


def is_valid_user_otp(user, otp: str) -> bool:
    try:
        user_otp = user.otp
        if user_otp.otp != otp:
            return False
        if user_otp.exp_time < timezone.now():
            return False
        return True
    except ObjectDoesNotExist:
        return False


def send_otp_email(user, otp) -> EmailMessage:
    context = {"fullname": user.full_name, "email": user.email, "otp": otp}
    message_body = get_template("otp_auth_template.html").render(context)
    send_email.delay(
        subject=Messages.OTP_EMAIL_SUBJECT,
        body=message_body,
        from_email=None,
        to=[user.email],
        reply_to=["noreply"],
        content_subtype="html",
    )
