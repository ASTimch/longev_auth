from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateUserSerializer,
    PasswordAuthSerializer,
    TokenSerializer,
    UpdateUserSerializer,
)
from core.constants import Messages
from core.utils import get_user_token

User = get_user_model()


class SignUpView(generics.CreateAPIView):
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


# class SignupView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         confirmation_code = default_token_generator.make_token(user)
#         # send_mail(
#         #     EMAIL_AUTHORIZATION_TITLE,
#         #     EMAIL_AUTHORIZATION_CONTENT.format(
#         #         username=user.username, confirmation_code=confirmation_code
#         #     ),
#         #     None,
#         #     [user.email],
#         #     fail_silently=False,
#         # )
#         return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordAuthView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=PasswordAuthSerializer, responses={200: TokenSerializer}
    )
    def post(self, request):
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


# class PasswordAuthView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = PasswordAuthSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = get_object_or_404(
#             User, username=serializer.validated_data["username"]
#         )
#         # validate confirmation_code
#         if not default_token_generator.check_token(
#             user, serializer.data["confirmation_code"]
#         ):
#             return Response(
#                 {"confirmation_code": INVALID_CONFIRMATION_CODE},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         jwt_token = str(RefreshToken.for_user(user).access_token)
#         response = {"token": jwt_token}
#         return Response(response, status=status.HTTP_200_OK)
