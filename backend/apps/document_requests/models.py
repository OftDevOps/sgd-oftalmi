from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentRequestType(models.TextChoices):
    CREATE = "create", _("Creation")
    MODIFY = "modify", _("Modification")
    REVIEW = "review", _("Review")
    OBSOLETE = "obsolete", _("Decommission / obsolescence")
    UPDATE = "update", _("Update")
    OTHER = "other", _("Other")


class DocumentRequestStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    SUBMITTED = "submitted", _("Submitted")
    RECEIVED = "received", _("Received by O&M")
    IN_REVIEW = "in_review", _("In review")
    OBSERVED = "observed", _("Observed")
    CANCELLED = "cancelled", _("Cancelled")
    CLOSED = "closed", _("Closed")


class DocumentRequest(models.Model):
    request_type = models.CharField(
        _("request type"),
        max_length=20,
        choices=DocumentRequestType.choices,
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=DocumentRequestStatus.choices,
        default=DocumentRequestStatus.DRAFT,
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("requested by"),
        on_delete=models.PROTECT,
        related_name="document_requests",
    )
    organizational_unit = models.ForeignKey(
        "organizational_units.OrganizationalUnit",
        verbose_name=_("organizational unit"),
        on_delete=models.PROTECT,
        related_name="document_requests",
    )
    document_type = models.ForeignKey(
        "document_types.DocumentType",
        verbose_name=_("document type"),
        on_delete=models.PROTECT,
        related_name="document_requests",
        blank=True,
        null=True,
    )
    related_document = models.ForeignKey(
        "documents.Document",
        verbose_name=_("related document"),
        on_delete=models.PROTECT,
        related_name="document_requests",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    submitted_at = models.DateTimeField(_("submitted at"), blank=True, null=True)
    closed_at = models.DateTimeField(_("closed at"), blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "document request"
        verbose_name_plural = "document requests"

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.title}"
