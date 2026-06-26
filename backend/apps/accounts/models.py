from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    OYM_ADMIN = "oym_admin", _("O&M functional administrator")
    OYM_ANALYST = "oym_analyst", _("O&M analyst")
    EXECUTING_UNIT = "executing_unit", _("Executing unit")
    READER = "reader", _("Reader")
    SYSTEMS_TECH_ADMIN = "systems_tech_admin", _("Systems technical administrator")
    AUDITOR = "auditor", _("Auditor")


ROLE_GROUP_NAMES = {
    UserRole.OYM_ADMIN: "OYM_ADMIN",
    UserRole.OYM_ANALYST: "OYM_ANALYST",
    UserRole.EXECUTING_UNIT: "EXECUTING_UNIT",
    UserRole.READER: "READER",
    UserRole.SYSTEMS_TECH_ADMIN: "SYSTEMS_TECH_ADMIN",
    UserRole.AUDITOR: "AUDITOR",
}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field is required.")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    role = models.CharField(
        _("role"),
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.READER,
    )
    organizational_unit = models.ForeignKey(
        "organizational_units.OrganizationalUnit",
        verbose_name=_("organizational unit"),
        on_delete=models.PROTECT,
        related_name="users",
        blank=True,
        null=True,
    )
    is_technical_user = models.BooleanField(_("technical user"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["email"]
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = type(self).objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        return self.first_name or self.email

    def get_role_group_name(self):
        return ROLE_GROUP_NAMES.get(self.role)

    def has_role(self, role):
        return self.role == role

    @property
    def is_oym_admin(self):
        return self.role == UserRole.OYM_ADMIN

    @property
    def is_oym_analyst(self):
        return self.role == UserRole.OYM_ANALYST

    @property
    def is_executing_unit_user(self):
        return self.role == UserRole.EXECUTING_UNIT

    @property
    def is_reader(self):
        return self.role == UserRole.READER

    @property
    def is_systems_tech_admin(self):
        return self.role == UserRole.SYSTEMS_TECH_ADMIN

    @property
    def is_auditor(self):
        return self.role == UserRole.AUDITOR
