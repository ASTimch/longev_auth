import base64
import os

import pyotp
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
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


def send_otp_email(user, otp):
    # send_mail(
    #     subject = "Authorization",
    #     message = "You login data: email {email}  otp_code {otp}".format(
    #         email=user.email, otp=otp
    #     ),
    #     None,
    #     [user.email],
    #     fail_silently=False,
    # )
    context = {"fullname": user.full_name, "email": user.email, "otp": otp}
    message = get_template("otp_auth_template.html").render(context)
    mail = EmailMessage(
        subject="Longevity authorization credentials",
        body=message,
        from_email=None,
        to=[user.email],
        reply_to=["noreply"],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=False)
