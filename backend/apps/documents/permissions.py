from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_admin, is_oym_user


VIEWABLE_DOCUMENT_STATUSES = {"published", "active"}
VIEWABLE_FILE_CONTENT_TYPES = {"application/pdf"}


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


def is_pdf_document_file(document_file):
    if not document_file:
        return False

    content_type = (document_file.content_type or "").lower()
    filename = (document_file.original_filename or "").lower()
    return content_type in VIEWABLE_FILE_CONTENT_TYPES or filename.endswith(".pdf")


def can_view_document_file(user, document_file):
    if not document_file or not document_file.is_active or not is_pdf_document_file(document_file):
        return False

    document_version = document_file.document_version
    document = document_version.document

    if can_view_obsolete_document(user):
        return True

    return has_any_role(
        user,
        {
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        },
    ) and (
        document.is_active
        and document.status in VIEWABLE_DOCUMENT_STATUSES
        and document_version.status in VIEWABLE_DOCUMENT_STATUSES
    )
