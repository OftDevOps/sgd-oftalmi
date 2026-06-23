from django.contrib import admin

from .models import DocumentRequest


@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_type",
        "title",
        "status",
        "organizational_unit",
        "requested_by",
        "created_at",
        "submitted_at",
        "closed_at",
    )
    list_filter = (
        "request_type",
        "status",
        "organizational_unit",
        "document_type",
        "created_at",
        "submitted_at",
        "closed_at",
    )
    search_fields = (
        "title",
        "description",
        "requested_by__email",
        "organizational_unit__name",
        "organizational_unit__code",
        "document_type__code",
        "document_type__name",
        "related_document__code",
        "related_document__title",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = (
        "requested_by",
        "organizational_unit",
        "document_type",
        "related_document",
    )
    list_select_related = (
        "requested_by",
        "organizational_unit",
        "document_type",
        "related_document",
    )
