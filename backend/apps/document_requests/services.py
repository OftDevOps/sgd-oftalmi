from django.utils import timezone

from .models import DocumentRequest, DocumentRequestStatus
from .workflows import validate_document_request_status_transition


def document_request_create(
    *,
    request_type,
    title,
    requested_by,
    organizational_unit,
    description="",
    document_type=None,
    related_document=None,
    status=None,
    submitted_at=None,
    closed_at=None,
):
    document_request = DocumentRequest(
        request_type=request_type,
        title=title,
        description=description,
        requested_by=requested_by,
        organizational_unit=organizational_unit,
        document_type=document_type,
        related_document=related_document,
        submitted_at=submitted_at,
        closed_at=closed_at,
    )
    if status is not None:
        document_request.status = status

    document_request.full_clean()
    document_request.save()
    return document_request


def document_request_transition_status(*, document_request, target_status, changed_at=None):
    validate_document_request_status_transition(document_request.status, target_status)

    changed_at = changed_at or timezone.now()
    update_fields = ["status", "updated_at"]

    document_request.status = target_status
    if target_status == DocumentRequestStatus.SUBMITTED and document_request.submitted_at is None:
        document_request.submitted_at = changed_at
        update_fields.append("submitted_at")
    if target_status == DocumentRequestStatus.CLOSED and document_request.closed_at is None:
        document_request.closed_at = changed_at
        update_fields.append("closed_at")

    document_request.full_clean()
    document_request.save(update_fields=update_fields)
    return document_request
