from django.core.exceptions import ValidationError

from apps.audit.models import AuditAction, AuditResult
from apps.audit.services import audit_event_create_for_instance, audit_event_create_if_requested

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
    audit_context=None,
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
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.DOCUMENT_CREATED,
        module="documents",
        instance=document,
        description="Document created.",
        after_data={
            "code": document.code,
            "title": document.title,
            "status": document.status,
        },
    )
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


def document_transition_status(*, document, target_status, audit_context=None):
    previous_status = document.status
    validate_document_status_transition(document.status, target_status)

    document.status = target_status
    document.full_clean()
    document.save(update_fields=["status", "updated_at"])
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.DOCUMENT_STATUS_CHANGED,
        module="documents",
        instance=document,
        description="Document status changed.",
        before_data={"status": previous_status},
        after_data={"status": document.status},
    )
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
    audit_context=None,
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
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.FILE_UPLOADED,
        module="documents",
        instance=document_file,
        description="Document file uploaded.",
        after_data={
            "document_version_id": document_version.id,
            "original_filename": original_filename,
            "content_type": content_type,
            "size_bytes": size_bytes,
            "file_hash": file_hash,
        },
    )
    return document_file


def document_file_access_audit_create(
    *,
    document_file,
    result,
    audit_context=None,
    description="Document file access.",
):
    if audit_context is None:
        return None

    document_version = document_file.document_version
    document = document_version.document
    return audit_event_create_for_instance(
        audit_context=audit_context,
        action=AuditAction.DOCUMENT_VIEWED,
        module="documents",
        instance=document_file,
        result=result,
        description=description,
        after_data={
            "document_id": document.id,
            "document_code": document.code,
            "document_version_id": document_version.id,
            "version_number": document_version.version_number,
            "document_file_id": document_file.id,
            "original_filename": document_file.original_filename,
        },
    )


def document_file_access_granted_audit_create(*, document_file, audit_context=None):
    return document_file_access_audit_create(
        document_file=document_file,
        audit_context=audit_context,
        result=AuditResult.SUCCESS,
        description="Controlled document file access granted.",
    )


def document_file_access_denied_audit_create(*, document_file, audit_context=None):
    return document_file_access_audit_create(
        document_file=document_file,
        audit_context=audit_context,
        result=AuditResult.DENIED,
        description="Controlled document file access denied.",
    )
