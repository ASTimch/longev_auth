from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import OtpCode
from core.constants import Messages

User = get_user_model()


class TestPasswordAuthView(APITestCase):
    """Login with email and password API case."""

    url = reverse("api:auth-token-pwd")

    @classmethod
    def setUpTestData(cls):
        cls.user1_raw_password = "user1password"
        cls.user1 = User.objects.create(
            email="user1@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=True,
            password=make_password(cls.user1_raw_password),
        )
        cls.inactive_user_raw_password = "user2password"
        cls.inactive_user = User.objects.create(
            email="user2@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=False,
            password=make_password(cls.inactive_user_raw_password),
        )

    def test_auth_with_correct_password(self):
        data = {
            "email": self.user1.email,
            "password": self.user1_raw_password,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_auth_with_incorrect_password(self):
        data = {
            "email": self.user1.email,
            "password": "wrongpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["message"], Messages.INCORRECT_PASSWORD
        )

    def test_auth_with_incorrect_email(self):
        data = {
            "email": "unknown@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auth_with_for_inactive_user(self):
        data = {
            "email": self.inactive_user.email,
            "password": self.inactive_user_raw_password,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["message"], Messages.PROFILE_IS_INACTIVE
        )


class TestOtpRequestView(APITestCase):
    """Login with email and otp API case."""

    url = reverse("api:auth-otp")

    @classmethod
    def setUpTestData(cls):
        cls.user1_raw_password = "user1password"
        cls.user1 = User.objects.create(
            email="user1@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=True,
            password=make_password(cls.user1_raw_password),
        )

    @patch("api.tasks.send_email.delay")
    def test_auth_get_otp_via_email(self, mock_task):
        data = {"email": self.user1.email}
        now = timezone.now()
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        mock_task.assert_called_once()
        expected_message = Messages.OTP_SENT_TO_EMAIL.format(
            email=self.user1.email
        )
        self.assertEquals(response.data["message"], expected_message)
        self.assert_(self.user1.otp)
        self.assertEquals(len(self.user1.otp.otp), 6)
        delta = self.user1.otp.exp_time - now
        self.assertAlmostEqual(
            delta.total_seconds(), settings.OTP_LIFETIME, delta=10
        )

    def test_auth_get_otp_for_unknown_email(self):
        data = {"email": "unknown@example.com"}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class TestOtpAuthView(APITestCase):
    """Login with email and otp API case."""

    url = reverse("api:auth-token-otp")

    @classmethod
    def setUpTestData(cls):
        cls.user1_raw_password = "user1password"
        cls.user1 = User.objects.create(
            email="user1@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=True,
            password=make_password(cls.user1_raw_password),
        )
        exp_time = timezone.now() + timedelta(minutes=10)
        cls.user1_otp = OtpCode.objects.create(
            user=cls.user1, otp="123456", exp_time=exp_time
        )

        cls.user2_raw_password = "user2password"
        cls.user2 = User.objects.create(
            email="user2@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=True,
            password=make_password(cls.user2_raw_password),
        )
        exp_time = timezone.now() - timedelta(seconds=5)
        cls.user2_otp = OtpCode.objects.create(
            user=cls.user2, otp="234567", exp_time=exp_time
        )

        cls.inactive_user_raw_password = "user3password"
        cls.inactive_user = User.objects.create(
            email="user3@example.com",
            first_name="firstname",
            last_name="lastname",
            is_active=False,
            password=make_password(cls.inactive_user_raw_password),
        )
        exp_time = timezone.now() + timedelta(minutes=10)
        cls.inactive_user_otp = OtpCode.objects.create(
            user=cls.inactive_user, otp="345678", exp_time=exp_time
        )

    def test_auth_with_correct_otp(self):
        data = {"email": self.user1.email, "otp": self.user1.otp.otp}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_auth_with_incorrect_otp(self):
        data = {
            "email": self.user1.email,
            "otp": "000000",
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["message"], Messages.INCORRECT_OTP)

    def test_otp_auth_with_incorrect_email(self):
        data = {
            "email": "unknown@example.com",
            "otp": self.user1.otp.otp,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auth_with_expired_otp(self):
        data = {
            "email": self.user2.email,
            "otp": self.user2.otp.otp,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data["message"], Messages.INCORRECT_OTP)

    def test_otp_auth_for_inactive_user(self):
        data = {
            "email": self.inactive_user.email,
            "otp": self.inactive_user.otp.otp,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["message"], Messages.PROFILE_IS_INACTIVE
        )
