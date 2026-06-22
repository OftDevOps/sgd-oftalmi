from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganizationalUnit(models.Model):
    name = models.CharField(_("name"), max_length=255)
    code = models.CharField(
        _("code"),
        max_length=50,
        unique=True,
        blank=True,
        null=True,
    )
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "organizational unit"
        verbose_name_plural = "organizational units"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = None

        super().save(*args, **kwargs)
