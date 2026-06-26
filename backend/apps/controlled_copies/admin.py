from django.contrib import admin

from .models import ControlledCopy


@admin.register(ControlledCopy)
class ControlledCopyAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "document_version",
        "copy_number",
        "receiver_unit",
        "receiver_user",
        "status",
        "delivered_at",
        "retired_at",
    )
    list_filter = (
        "status",
        "receiver_unit",
        "document",
        "delivered_at",
        "retired_at",
        "created_at",
    )
    search_fields = (
        "copy_number",
        "document__code",
        "document__title",
        "document_version__version_number",
        "receiver_unit__code",
        "receiver_unit__name",
        "receiver_user__email",
        "created_by__email",
        "observations",
        "evidence_reference",
    )
    ordering = ("document__code", "copy_number")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = (
        "document",
        "document_version",
        "receiver_unit",
        "receiver_user",
        "created_by",
    )
    list_select_related = (
        "document",
        "document_version",
        "receiver_unit",
        "receiver_user",
        "created_by",
    )
