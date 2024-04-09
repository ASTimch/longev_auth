from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OtpCode
from .serializers import (
    CreateUserSerializer,
    OtpAuthSerializer,
    OtpRequestSerializer,
    PasswordAuthSerializer,
    TokenSerializer,
    UpdateUserSerializer,
)
from core.constants import Messages
from core.utils import generate_otp_code, get_user_token, is_valid_user_otp

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    """Create new user."""

    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Allows retrieve, update and delete user profile."""

    serializer_class = UpdateUserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Get authorized user profile."""
        return self.request.user

    def put(self, request, *args, **kwargs):
        """Update user profile."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": serializer.data, "message": Messages.PROFILE_UPDATED},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        """Delete user profile."""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {"message": Messages.PROFILE_DELETED},
            status=status.HTTP_204_NO_CONTENT,
        )


class PasswordAuthView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=PasswordAuthSerializer, responses={200: TokenSerializer}
    )
    def post(self, request):
        """Return jwt token for given email and password."""
        serializer = PasswordAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = get_object_or_404(User, email=email)
        if not user.is_active:
            raise ValidationError({"message": Messages.PROFILE_IS_INACTIVE})
        if not check_password(password, user.password):
            raise ValidationError({"message": Messages.INCORRECT_PASSWORD})
        token_data = get_user_token(user)
        return Response(token_data, status=status.HTTP_200_OK)


class OtpRequestView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=OtpRequestSerializer)
    def post(self, request):
        """Generate otp code and send to given email."""
        serializer = OtpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)
        if not user.is_active:
            raise ValidationError({"message": Messages.PROFILE_IS_INACTIVE})
        try:
            user.otp.delete()
        except ObjectDoesNotExist:
            pass
        otp = generate_otp_code()
        exp_time = timezone.now() + timedelta(minutes=settings.OTP_LIFETIME)
        otp_model = OtpCode(otp=otp, user=user, exp_time=exp_time)
        otp_model.save()
        send_mail(
            "Authorization",
            "You login data: email {email}  otp_code {otp}".format(
                email=user.email, otp=otp
            ),
            None,
            [user.email],
            fail_silently=False,
        )
        return Response(
            {"message": Messages.OTP_SENT_TO_EMAIL.format(email=user.email)},
            status=status.HTTP_200_OK,
        )


class OtpAuthView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=OtpAuthSerializer, responses={200: TokenSerializer}
    )
    def post(self, request):
        """Return jwt token for given email and otp code."""
        serializer = OtpAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        user = get_object_or_404(User, email=email)
        if not user.is_active:
            raise ValidationError({"message": Messages.PROFILE_IS_INACTIVE})
        if not is_valid_user_otp(user, otp):
            raise ValidationError({"message": Messages.INCORRECT_OTP})
        user.otp.delete()
        user.save()
        token_data = get_user_token(user)
        return Response(token_data, status=status.HTTP_200_OK)
