from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class OTPLoginFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="Secret123!",
        )

    def test_login_requires_otp_verification(self):
        response = self.client.post(
            reverse("login"),
            {"username": "alice", "password": "Secret123!"},
            follow=True,
        )

        self.assertRedirects(response, reverse("verify_otp"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(len(mail.outbox), 1)

        otp = self.user.otps.order_by("-created_at").first()
        self.assertIsNotNone(otp)
        self.assertEqual(len(otp.otp_code), 6)

    def test_valid_otp_logs_user_in(self):
        self.client.post(
            reverse("login"),
            {"username": "alice", "password": "Secret123!"},
        )

        otp = self.user.otps.order_by("-created_at").first()
        response = self.client.post(
            reverse("verify_otp"),
            {"otp_code": otp.otp_code},
            follow=True,
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_invalid_otp_blocks_access(self):
        self.client.post(
            reverse("login"),
            {"username": "alice", "password": "Secret123!"},
        )

        response = self.client.post(
            reverse("verify_otp"),
            {"otp_code": "123456"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "invalid or expired")
