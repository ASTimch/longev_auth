from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.constants import Limits, Messages

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=Limits.EMAIL_LENGTH,
        validators=[
            EmailValidator(),
            UniqueValidator(
                queryset=User.objects.all(),
                message=Messages.EMAIL_ALREADY_EXISTS,
            ),
        ],
    )
    password = serializers.CharField(
        min_length=Limits.MIN_PASSWORD_LENGTH,
        max_length=Limits.MAX_PASSWORD_LENGTH,
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        read_only_fields = ("email",)


class PasswordAuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}
    )


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class OtpRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class OtpAuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
