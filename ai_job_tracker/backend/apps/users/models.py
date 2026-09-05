import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class UserOTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps",
    )
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def generate_for_user(cls, user):
        otp_code = str(random.randint(000000, 999999))
        expires_at = timezone.now() + timedelta(minutes=1)

        return cls.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at,
        )

    def is_valid(self, submitted_code):
        return (
            self.otp_code == submitted_code
            and self.used_at is None
            and timezone.now() < self.expires_at
        )
