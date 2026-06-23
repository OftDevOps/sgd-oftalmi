from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class DocumentStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    RECEIVED = "received", _("Received")
    UNDER_REVIEW = "under_review", _("Under review")
    OBSERVED = "observed", _("Observed")
    APPROVED = "approved", _("Approved")
    PUBLISHED = "published", _("Published")
    ACTIVE = "active", _("Active")
    EXPIRED = "expired", _("Expired")
    OBSOLETE = "obsolete", _("Obsolete")
    ARCHIVED = "archived", _("Archived")


class Document(models.Model):
    code = models.CharField(_("code"), max_length=100, unique=True)
    title = models.CharField(_("title"), max_length=255)
    document_type = models.ForeignKey(
        "document_types.DocumentType",
        verbose_name=_("document type"),
        on_delete=models.PROTECT,
        related_name="documents",
    )
    owner_unit = models.ForeignKey(
        "organizational_units.OrganizationalUnit",
        verbose_name=_("owner unit"),
        on_delete=models.PROTECT,
        related_name="owned_documents",
    )
    current_version = models.ForeignKey(
        "documents.DocumentVersion",
        verbose_name=_("current version"),
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.DRAFT,
    )
    is_active = models.BooleanField(_("active"), default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        on_delete=models.PROTECT,
        related_name="created_documents",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "document"
        verbose_name_plural = "documents"

    def __str__(self):
        return f"{self.code} - {self.title}"


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        verbose_name=_("document"),
        on_delete=models.CASCADE,
        related_name="versions",
    )
    version_number = models.CharField(_("version number"), max_length=50)
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.DRAFT,
    )
    issue_date = models.DateField(_("issue date"), blank=True, null=True)
    effective_date = models.DateField(_("effective date"), blank=True, null=True)
    expiration_date = models.DateField(_("expiration date"), blank=True, null=True)
    approved_at = models.DateTimeField(_("approved at"), blank=True, null=True)
    published_at = models.DateTimeField(_("published at"), blank=True, null=True)
    obsolete_at = models.DateTimeField(_("obsolete at"), blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        on_delete=models.PROTECT,
        related_name="created_document_versions",
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "version_number"],
                name="unique_document_version_number",
            ),
        ]
        ordering = ["document__code", "version_number"]
        verbose_name = "document version"
        verbose_name_plural = "document versions"

    def __str__(self):
        return f"{self.document.code} v{self.version_number}"


class DocumentFile(models.Model):
    document_version = models.ForeignKey(
        DocumentVersion,
        verbose_name=_("document version"),
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.FileField(_("file"), upload_to="documents/%Y/%m/")
    original_filename = models.CharField(_("original filename"), max_length=255)
    content_type = models.CharField(_("content type"), max_length=100, blank=True)
    size_bytes = models.PositiveBigIntegerField(
        _("size bytes"),
        blank=True,
        null=True,
    )
    file_hash = models.CharField(_("file hash"), max_length=128, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("uploaded by"),
        on_delete=models.PROTECT,
        related_name="uploaded_document_files",
    )
    uploaded_at = models.DateTimeField(_("uploaded at"), auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "document file"
        verbose_name_plural = "document files"

    def __str__(self):
        return self.original_filename


class DocumentCodeSequence(models.Model):
    document_type = models.ForeignKey(
        "document_types.DocumentType",
        verbose_name=_("document type"),
        on_delete=models.PROTECT,
        related_name="code_sequences",
    )
    organizational_unit = models.ForeignKey(
        "organizational_units.OrganizationalUnit",
        verbose_name=_("organizational unit"),
        on_delete=models.PROTECT,
        related_name="document_code_sequences",
        blank=True,
        null=True,
    )
    prefix = models.CharField(_("prefix"), max_length=50)
    current_number = models.PositiveIntegerField(_("current number"))
    padding = models.PositiveSmallIntegerField(_("padding"))
    is_active = models.BooleanField(_("active"), default=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "organizational_unit", "prefix"],
                condition=Q(organizational_unit__isnull=False),
                name="unique_code_sequence_with_unit",
            ),
            models.UniqueConstraint(
                fields=["document_type", "prefix"],
                condition=Q(organizational_unit__isnull=True),
                name="unique_code_sequence_without_unit",
            ),
        ]
        ordering = ["document_type__code", "organizational_unit__code", "prefix"]
        verbose_name = "document code sequence"
        verbose_name_plural = "document code sequences"

    def __str__(self):
        unit_code = self.organizational_unit.code if self.organizational_unit else "GLOBAL"
        return f"{self.document_type.code}-{unit_code}-{self.prefix}"
