from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class SignUpViewTest(APITestCase):
    """Signup new user API tests."""

    url_signup = reverse("api:user-signup")

    def setUp(self):
        """Create one user."""
        self.user1 = User.objects.create(
            email="user1@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=True,
            password=make_password("user1password"),
        )

    def test_signup_ok(self):
        """Test signup success for valid entry."""
        data = {
            "email": "user2@example.com",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": "user2password",
        }
        response = self.client.post(self.url_signup, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.filter(email=data["email"]).first()
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(
            user.full_name, data["first_name"] + " " + data["last_name"]
        )

    def test_signup_failed_for_invalid_email(self):
        data = {
            "email": "bademail",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": "user2password",
        }
        response = self.client.post(self.url_signup, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_failed_without_email(self):
        data = {
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": "user2password",
        }
        response = self.client.post(self.url_signup, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_failed_for_duplicate_email(self):
        data = {
            "email": self.user1.email,
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": "user2password",
        }
        response = self.client.post(self.url_signup, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_failed_without_password(self):
        data = {
            "email": "somemail@example.com",
            "first_name": "Firstname",
            "last_name": "Lastname",
        }
        response = self.client.post(self.url_signup, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_failed_for_short_password(self):
        """Fail for password shorter than 8 characters."""
        data = {
            "email": "somemail@example.com",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": "1234567",
        }
        response = self.client.post(self.url_signup, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
