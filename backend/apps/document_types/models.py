from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentType(models.Model):
    code = models.CharField(_("code"), max_length=50, unique=True)
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "document type"
        verbose_name_plural = "document types"

    def __str__(self):
        return f"{self.code} - {self.name}"
