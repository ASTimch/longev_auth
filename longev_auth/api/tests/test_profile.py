from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User


class ProfileViewTest(APITestCase):
    """User Profile get, update, delete API tests."""

    url_profile = reverse("api:user-profile")

    def setUp(self):
        """Create 2 users."""
        self.user1 = User.objects.create(
            email="user1@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=True,
            password="user1password",
        )
        self.user1.set_password("user1password")

        self.user2 = User.objects.create(
            email="user2@example.com",
            first_name="Anotherfirstname",
            last_name="Anotherlastname",
            is_active=True,
            password="user2password",
        )
        self.user2.set_password("user2password")

        self.user1client = APIClient()
        self.user1client.force_authenticate(user=self.user1)
        self.anonymous_client = APIClient()

    def test_get_profile_for_authorized_user(self):
        response = self.user1client.get(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user1.email)
        self.assertEqual(response.data["first_name"], self.user1.first_name)
        self.assertEqual(response.data["last_name"], self.user1.last_name)

    def test_patch_first_name_profile_for_authorized_user(self):
        new_first_name = "newname"
        data = {"first_name": new_first_name}
        response = self.user1client.patch(self.url_profile, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user1.email)
        self.assertEqual(response.data["first_name"], self.user1.first_name)
        self.assertEqual(response.data["first_name"], new_first_name)
        self.assertEqual(response.data["last_name"], self.user1.last_name)

    def test_patch_last_name_profile_for_authorized_user(self):
        new_last_name = "newlastname"
        data = {"last_name": new_last_name}
        response = self.user1client.patch(self.url_profile, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user1.email)
        self.assertEqual(response.data["first_name"], self.user1.first_name)
        self.assertEqual(response.data["last_name"], new_last_name)
        self.assertEqual(response.data["last_name"], self.user1.last_name)

    def test_put_profile_for_authorized_user(self):
        new_first_name = "newfirstname"
        new_last_name = "newlastname"
        data = {"first_name": new_first_name, "last_name": new_last_name}
        response = self.user1client.put(self.url_profile, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user1.email)
        self.assertEqual(response.data["first_name"], new_first_name)
        self.assertEqual(response.data["first_name"], self.user1.first_name)
        self.assertEqual(response.data["last_name"], new_last_name)
        self.assertEqual(response.data["last_name"], self.user1.last_name)

    def test_put_profile_for_authorized_user(self):
        new_first_name = "newfirstname"
        new_last_name = "newlastname"
        data = {
            "first_name": new_first_name,
            "last_name": new_last_name,
        }
        response = self.user1client.put(self.url_profile, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user1.email)
        self.assertEqual(response.data["first_name"], new_first_name)
        self.assertEqual(response.data["first_name"], self.user1.first_name)
        self.assertEqual(response.data["last_name"], new_last_name)
        self.assertEqual(response.data["last_name"], self.user1.last_name)

    def test_delete_profile_for_authorized_user(self):
        response = self.user1client.delete(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user1.is_active, False)
        self.assertEqual(response.data["message"], "Profile has been deleted")

    def test_get_profile_for_anonymous_client(self):
        response = self.anonymous_client.get(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_for_anonymous_client(self):
        response = self.anonymous_client.patch(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_profile_for_anonymous_client(self):
        response = self.anonymous_client.put(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_profile_for_anonymous_client(self):
        response = self.anonymous_client.delete(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
