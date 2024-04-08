from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "authentication"

router = DefaultRouter()

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
]
