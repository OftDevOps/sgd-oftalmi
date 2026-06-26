from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "module",
        "action",
        "result",
        "user",
        "entity_type",
        "entity_id",
        "ip_address",
    )
    list_filter = ("action", "result", "module", "created_at")
    search_fields = (
        "module",
        "entity_type",
        "entity_id",
        "user__email",
        "description",
        "ip_address",
    )
    ordering = ("-created_at",)
    readonly_fields = (
        "user",
        "action",
        "module",
        "entity_type",
        "entity_id",
        "result",
        "ip_address",
        "user_agent",
        "description",
        "before_data",
        "after_data",
        "created_at",
    )
    raw_id_fields = ("user",)
    list_select_related = ("user",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
