from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_admin


def can_view_document_types(user):
    return has_any_role(
        user,
        {UserRole.OYM_ADMIN, UserRole.OYM_ANALYST, UserRole.EXECUTING_UNIT},
    )


def can_manage_document_types(user):
    return is_oym_admin(user)
