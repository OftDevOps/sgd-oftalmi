from django.core.exceptions import ValidationError

from .models import Document, DocumentFile, DocumentVersion
from .workflows import validate_document_status_transition


def document_create(
    *,
    code,
    title,
    document_type,
    owner_unit,
    created_by,
    status=None,
    is_active=True,
):
    document = Document(
        code=code,
        title=title,
        document_type=document_type,
        owner_unit=owner_unit,
        created_by=created_by,
        is_active=is_active,
    )
    if status is not None:
        document.status = status

    document.full_clean()
    document.save()
    return document


def document_version_create(*, document, version_number, created_by, status=None, **dates):
    document_version = DocumentVersion(
        document=document,
        version_number=version_number,
        created_by=created_by,
        **dates,
    )
    if status is not None:
        document_version.status = status

    document_version.full_clean()
    document_version.save()
    return document_version


def document_set_current_version(*, document, document_version):
    if document_version.document_id != document.id:
        raise ValidationError("The current version must belong to the selected document.")

    document.current_version = document_version
    document.full_clean()
    document.save(update_fields=["current_version", "updated_at"])
    return document


def document_transition_status(*, document, target_status):
    validate_document_status_transition(document.status, target_status)

    document.status = target_status
    document.full_clean()
    document.save(update_fields=["status", "updated_at"])
    return document


def document_file_create(
    *,
    document_version,
    file,
    original_filename,
    uploaded_by,
    content_type="",
    size_bytes=None,
    file_hash="",
    is_active=True,
):
    document_file = DocumentFile(
        document_version=document_version,
        file=file,
        original_filename=original_filename,
        content_type=content_type,
        size_bytes=size_bytes,
        file_hash=file_hash,
        uploaded_by=uploaded_by,
        is_active=is_active,
    )
    document_file.full_clean()
    document_file.save()
    return document_file
