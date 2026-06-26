from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_active_user, is_oym_user


def can_view_own_notifications(user):
    return is_active_user(user)


def can_manage_functional_notifications(user):
    return is_oym_user(user)


def can_manage_email_settings(user):
    return has_any_role(user, {UserRole.SYSTEMS_TECH_ADMIN})
