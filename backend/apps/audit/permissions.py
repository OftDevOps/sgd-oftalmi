from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role


def can_view_functional_audit(user):
    return has_any_role(
        user,
        {
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.AUDITOR,
        },
    )


def can_view_technical_audit(user):
    return has_any_role(user, {UserRole.SYSTEMS_TECH_ADMIN})


def can_export_audit(user):
    return has_any_role(user, {UserRole.OYM_ADMIN, UserRole.AUDITOR})


def can_modify_audit(user):
    return False


def can_view_audit(user):
    return can_view_functional_audit(user) or can_view_technical_audit(user)
