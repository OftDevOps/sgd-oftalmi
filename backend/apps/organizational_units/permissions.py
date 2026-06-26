from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_admin


def can_view_organizational_units(user):
    return has_any_role(
        user,
        {UserRole.OYM_ADMIN, UserRole.OYM_ANALYST, UserRole.SYSTEMS_TECH_ADMIN},
    )


def can_manage_organizational_units(user):
    return is_oym_admin(user)
