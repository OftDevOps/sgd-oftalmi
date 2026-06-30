from django.urls import reverse

from .models import UserRole


ROLE_HOME_URL_NAMES = {
    UserRole.OYM_ADMIN: "app:documents:index",
    UserRole.OYM_ANALYST: "app:documents:index",
    UserRole.EXECUTING_UNIT: "app:document_requests:index",
    UserRole.READER: "app:documents:index",
    UserRole.SYSTEMS_TECH_ADMIN: "app:accounts:index",
    UserRole.AUDITOR: "app:audit:index",
}


def get_role_home_url(user):
    if not user or not user.is_authenticated:
        return reverse("login")

    return reverse(ROLE_HOME_URL_NAMES.get(user.role, "app:dashboard"))
