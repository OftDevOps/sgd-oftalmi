from apps.accounts.permissions import is_oym_user


def can_manage_controlled_copies(user):
    return is_oym_user(user)


def can_register_controlled_copy(user):
    return is_oym_user(user)


def can_register_controlled_copy_delivery(user):
    return is_oym_user(user)


def can_register_controlled_copy_retirement(user):
    return is_oym_user(user)


def can_view_controlled_copies(user):
    return is_oym_user(user)
