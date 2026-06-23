from django.contrib import admin

from .models import Document, DocumentFile, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "document_type", "owner_unit", "status", "is_active")
    list_filter = ("status", "is_active", "document_type", "owner_unit")
    search_fields = ("code", "title")
    ordering = ("code",)
    raw_id_fields = ("current_version", "created_by")
    list_select_related = ("document_type", "owner_unit", "current_version", "created_by")


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ("document", "version_number", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("document__code", "document__title", "version_number")
    ordering = ("document__code", "version_number")
    raw_id_fields = ("document", "created_by")
    list_select_related = ("document", "created_by")


@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "document_version",
        "content_type",
        "size_bytes",
        "is_active",
        "uploaded_at",
    )
    list_filter = ("is_active", "content_type")
    search_fields = (
        "original_filename",
        "file_hash",
        "document_version__document__code",
        "document_version__version_number",
    )
    ordering = ("-uploaded_at",)
    raw_id_fields = ("document_version", "uploaded_by")
    list_select_related = ("document_version", "uploaded_by")
