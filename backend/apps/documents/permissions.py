from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_admin, is_oym_user


def can_create_document(user):
    return is_oym_user(user)


def can_edit_document_metadata(user):
    return is_oym_user(user)


def can_upload_document_file(user):
    return is_oym_user(user)


def can_publish_document(user):
    return is_oym_admin(user)


def can_view_assigned_document(user, *, is_assigned=False):
    return has_any_role(
        user,
        {
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        },
    ) and (is_oym_user(user) or is_assigned)


def can_view_obsolete_document(user):
    return is_oym_user(user)


def can_decommission_document(user):
    return is_oym_admin(user)


def can_download_document(user):
    return False


def can_print_document(user):
    return False


def can_copy_document(user):
    return False
