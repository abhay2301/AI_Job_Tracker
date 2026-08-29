from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "position",
        "status",
        "application_date",
        "user",
    )

    list_filter = (
        "status",
        "application_date",
    )

    search_fields = (
        "company",
        "position",
        "user__username",
    )