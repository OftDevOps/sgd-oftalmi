from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class ControlledCopyStatus(models.TextChoices):
    REGISTERED = "registered", _("Registered")
    DELIVERED = "delivered", _("Delivered")
    ACTIVE = "active", _("Active")
    RETIRED = "retired", _("Retired")
    CANCELLED = "cancelled", _("Cancelled")


class ControlledCopy(models.Model):
    document = models.ForeignKey(
        "documents.Document",
        verbose_name=_("document"),
        on_delete=models.PROTECT,
        related_name="controlled_copies",
    )
    document_version = models.ForeignKey(
        "documents.DocumentVersion",
        verbose_name=_("document version"),
        on_delete=models.PROTECT,
        related_name="controlled_copies",
    )
    copy_number = models.CharField(_("copy number"), max_length=50)
    receiver_unit = models.ForeignKey(
        "organizational_units.OrganizationalUnit",
        verbose_name=_("receiver unit"),
        on_delete=models.PROTECT,
        related_name="received_controlled_copies",
    )
    receiver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("receiver user"),
        on_delete=models.PROTECT,
        related_name="received_controlled_copies",
        blank=True,
        null=True,
    )
    delivered_at = models.DateTimeField(_("delivered at"), blank=True, null=True)
    retired_at = models.DateTimeField(_("retired at"), blank=True, null=True)
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=ControlledCopyStatus.choices,
        default=ControlledCopyStatus.REGISTERED,
    )
    observations = models.TextField(_("observations"), blank=True)
    evidence_reference = models.CharField(_("evidence reference"), max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        on_delete=models.PROTECT,
        related_name="created_controlled_copies",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_version", "copy_number"],
                name="unique_controlled_copy_number_per_version",
            ),
        ]
        ordering = ["document__code", "copy_number"]
        verbose_name = "controlled copy"
        verbose_name_plural = "controlled copies"

    def __str__(self):
        return f"{self.document.code} - copy {self.copy_number}"

    def clean(self):
        super().clean()
        if (
            self.document_id
            and self.document_version_id
            and self.document_version.document_id != self.document_id
        ):
            raise ValidationError(
                {
                    "document_version": _(
                        "The document version must belong to the selected document."
                    )
                }
            )
