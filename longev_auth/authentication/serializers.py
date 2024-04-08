from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer

User = get_user_model()


class CustomCurrentUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name")
        read_only_fields = ("id", "email")
