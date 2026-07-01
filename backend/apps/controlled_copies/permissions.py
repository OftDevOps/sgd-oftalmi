from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_user


def can_manage_controlled_copies(user):
    return is_oym_user(user)


def can_register_controlled_copy(user):
    return is_oym_user(user)


def can_register_controlled_copy_delivery(user):
    return is_oym_user(user)


def can_register_controlled_copy_retirement(user):
    return is_oym_user(user)


def can_view_controlled_copies(user):
    return has_any_role(
        user,
        {
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        },
    )
