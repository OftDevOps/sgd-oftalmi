from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditAction(models.TextChoices):
    LOGIN = "login", _("Login")
    LOGOUT = "logout", _("Logout")
    DOCUMENT_CREATED = "document_created", _("Document created")
    DOCUMENT_UPDATED = "document_updated", _("Document updated")
    DOCUMENT_STATUS_CHANGED = "document_status_changed", _("Document status changed")
    FILE_UPLOADED = "file_uploaded", _("File uploaded")
    DOCUMENT_VIEWED = "document_viewed", _("Document viewed")
    REQUEST_REGISTERED = "request_registered", _("Request registered")
    REQUEST_APPROVED = "request_approved", _("Request approved")
    REQUEST_REJECTED = "request_rejected", _("Request rejected")
    IMPLEMENTATION_RECORD_REGISTERED = (
        "implementation_record_registered",
        _("Implementation record registered"),
    )
    CONTROLLED_COPY_DELIVERED = "controlled_copy_delivered", _("Controlled copy delivered")
    CONTROLLED_COPY_RETIRED = "controlled_copy_retired", _("Controlled copy retired")
    REPORT_GENERATED = "report_generated", _("Report generated")
    PERMISSION_CHANGED = "permission_changed", _("Permission changed")
    OTHER = "other", _("Other")


class AuditResult(models.TextChoices):
    SUCCESS = "success", _("Success")
    FAILURE = "failure", _("Failure")
    DENIED = "denied", _("Denied")
    WARNING = "warning", _("Warning")


class AuditEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.SET_NULL,
        related_name="audit_events",
        blank=True,
        null=True,
    )
    action = models.CharField(_("action"), max_length=50, choices=AuditAction.choices)
    module = models.CharField(_("module"), max_length=100)
    entity_type = models.CharField(_("entity type"), max_length=100, blank=True)
    entity_id = models.CharField(_("entity id"), max_length=100, blank=True)
    result = models.CharField(_("result"), max_length=20, choices=AuditResult.choices)
    ip_address = models.GenericIPAddressField(_("IP address"), blank=True, null=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    description = models.TextField(_("description"), blank=True)
    before_data = models.JSONField(_("before data"), blank=True, null=True)
    after_data = models.JSONField(_("after data"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "audit event"
        verbose_name_plural = "audit events"

    def __str__(self):
        return f"{self.module} - {self.get_action_display()} - {self.get_result_display()}"
