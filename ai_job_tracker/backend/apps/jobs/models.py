from django.conf import settings
from django.db import models


class JobApplication(models.Model):

    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        ASSESSMENT = "assessment", "Assessment"
        INTERVIEW = "interview", "Interview"
        REJECTED = "rejected", "Rejected"
        SELECTED = "selected", "Selected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )

    company = models.CharField(max_length=200)

    position = models.CharField(max_length=200)

    job_url = models.URLField(
        blank=True,
        null=True,
    )

    job_description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SAVED,
    )

    application_date = models.DateField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.company} - {self.position}"