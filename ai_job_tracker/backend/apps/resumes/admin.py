from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "uploaded_at",
        "updated_at",
    )

    list_filter = (
        "uploaded_at",
    )

    search_fields = (
        "title",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "extracted_text",
        "uploaded_at",
        "updated_at",
    )