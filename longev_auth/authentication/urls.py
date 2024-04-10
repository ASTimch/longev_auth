from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    OtpAuthView,
    OtpRequestView,
    PasswordAuthView,
    ProfileView,
    SignUpView,
)

app_name = "authentication"

router = DefaultRouter()


user_urlpatterns = [
    path("signup/", SignUpView.as_view(), name="user-signup"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
]

auth_urlpatterns = [
    path("token-pwd/", PasswordAuthView.as_view(), name="auth-token-pwd"),
    path("otp/", OtpRequestView.as_view(), name="auth-otp"),
    path("token-otp/", OtpAuthView.as_view(), name="auth-token-otp"),
]

urlpatterns = [
    path("user/", include(user_urlpatterns)),
    path("auth/", include(auth_urlpatterns)),
]
