from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ImplementationRecordStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    READ = "read", _("Read")
    INTERPRETED = "interpreted", _("Interpreted")
    ACCEPTED = "accepted", _("Accepted")
    IMPLEMENTED = "implemented", _("Implemented")
    EXPIRED = "expired", _("Expired")
    CANCELLED = "cancelled", _("Cancelled")


class ImplementationRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.PROTECT,
        related_name="implementation_records",
    )
    document = models.ForeignKey(
        "documents.Document",
        verbose_name=_("document"),
        on_delete=models.PROTECT,
        related_name="implementation_records",
    )
    document_version = models.ForeignKey(
        "documents.DocumentVersion",
        verbose_name=_("document version"),
        on_delete=models.PROTECT,
        related_name="implementation_records",
    )
    assigned_at = models.DateTimeField(_("assigned at"), default=timezone.now)
    read_at = models.DateTimeField(_("read at"), blank=True, null=True)
    interpreted_at = models.DateTimeField(_("interpreted at"), blank=True, null=True)
    accepted_at = models.DateTimeField(_("accepted at"), blank=True, null=True)
    implemented_at = models.DateTimeField(_("implemented at"), blank=True, null=True)
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=ImplementationRecordStatus.choices,
        default=ImplementationRecordStatus.PENDING,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "document_version"],
                name="unique_implementation_record_per_user_version",
            ),
        ]
        ordering = ["document__code", "document_version__version_number", "user__email"]
        verbose_name = "implementation record"
        verbose_name_plural = "implementation records"

    def __str__(self):
        return f"{self.user.email} - {self.document.code} v{self.document_version.version_number}"

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
