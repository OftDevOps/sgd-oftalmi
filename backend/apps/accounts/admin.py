from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import ROLE_GROUP_NAMES, User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
            "organizational_unit",
            "is_technical_user",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        return User.objects.normalize_email(email)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "organizational_unit",
            "is_technical_user",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "organizational_unit",
        "is_technical_user",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "role",
        "organizational_unit",
        "is_technical_user",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    raw_id_fields = ("organizational_unit",)
    list_select_related = ("organizational_unit",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "organizational_unit")},
        ),
        (_("Role"), {"fields": ("role", "is_technical_user")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "updated_at")}),
    )
    readonly_fields = ("date_joined", "updated_at", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "organizational_unit",
                    "is_technical_user",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group_name = obj.get_role_group_name()
        if not group_name:
            return

        group, _ = obj.groups.model.objects.get_or_create(name=group_name)
        managed_group_names = set(ROLE_GROUP_NAMES.values())
        obj.groups.remove(*obj.groups.filter(name__in=managed_group_names))
        obj.groups.add(group)
