from django.contrib import admin

from .models import ImplementationRecord


@admin.register(ImplementationRecord)
class ImplementationRecordAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "document",
        "document_version",
        "status",
        "assigned_at",
        "read_at",
        "accepted_at",
        "implemented_at",
    )
    list_filter = (
        "status",
        "document",
        "assigned_at",
        "read_at",
        "accepted_at",
        "implemented_at",
        "created_at",
    )
    search_fields = (
        "user__email",
        "document__code",
        "document__title",
        "document_version__version_number",
    )
    ordering = ("document__code", "document_version__version_number", "user__email")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user", "document", "document_version")
    list_select_related = ("user", "document", "document_version")
