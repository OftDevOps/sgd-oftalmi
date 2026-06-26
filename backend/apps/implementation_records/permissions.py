from apps.accounts.permissions import is_oym_user, is_active_user


def can_view_own_implementation_record(user, implementation_record):
    return is_active_user(user) and implementation_record.user_id == user.id


def can_confirm_own_implementation_record(user, implementation_record):
    return can_view_own_implementation_record(user, implementation_record)


def can_view_implementation_records_by_document(user):
    return is_oym_user(user)


def can_report_pending_implementation_records(user):
    return is_oym_user(user)
