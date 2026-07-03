from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_admin, is_oym_user


VIEWABLE_DOCUMENT_STATUSES = {"published", "active"}
VIEWABLE_FILE_CONTENT_TYPES = {"application/pdf"}
ACTIVE_CONTROLLED_COPY_STATUSES = {"active", "delivered"}


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


def is_viewable_document_version(document, document_version):
    return (
        document.is_active
        and document.status in VIEWABLE_DOCUMENT_STATUSES
        and document_version.status in VIEWABLE_DOCUMENT_STATUSES
    )


def has_direct_document_version_relation(user, document, document_version):
    if not user or not user.is_authenticated:
        return False

    from apps.controlled_copies.models import ControlledCopy
    from apps.implementation_records.models import ImplementationRecord

    return (
        ImplementationRecord.objects.filter(
            user=user,
            document=document,
            document_version=document_version,
        ).exists()
        or ControlledCopy.objects.filter(
            receiver_user=user,
            document=document,
            document_version=document_version,
            status__in=ACTIVE_CONTROLLED_COPY_STATUSES,
        ).exists()
    )


def has_unit_document_version_relation(user, document, document_version):
    if not user or not user.is_authenticated or not user.organizational_unit_id:
        return False

    from apps.controlled_copies.models import ControlledCopy

    return (
        document.owner_unit_id == user.organizational_unit_id
        or ControlledCopy.objects.filter(
            receiver_unit_id=user.organizational_unit_id,
            document=document,
            document_version=document_version,
            status__in=ACTIVE_CONTROLLED_COPY_STATUSES,
        ).exists()
    )


def can_view_document_file(user, document_file):
    if (
        not document_file
        or not document_file.is_active
        or not is_pdf_document_file(document_file)
    ):
        return False

    document_version = document_file.document_version
    document = document_version.document

    if can_view_obsolete_document(user):
        return True

    if not is_viewable_document_version(document, document_version):
        return False

    if has_direct_document_version_relation(user, document, document_version):
        return True

    if has_any_role(user, {UserRole.EXECUTING_UNIT}) and has_unit_document_version_relation(
        user,
        document,
        document_version,
    ):
        return True

    return has_any_role(
        user,
        {UserRole.READER},
    ) and has_unit_document_version_relation(
        user,
        document,
        document_version,
    )
