from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PasswordAuthView, ProfileView, SignUpView

app_name = "authentication"

router = DefaultRouter()


user_urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("profile/", ProfileView.as_view()),
]

auth_urlpatterns = [
    path("token-pwd/", PasswordAuthView.as_view()),
    # path("token-otp/", AuthView.as_view()),
]

urlpatterns = [
    path("", include(user_urlpatterns)),
    path("auth/", include(auth_urlpatterns)),
]
