from apps.accounts.permissions import is_oym_user


def can_view_reports(user):
    return is_oym_user(user)


def can_generate_reports(user):
    return is_oym_user(user)


def can_export_reports(user):
    return is_oym_user(user)
