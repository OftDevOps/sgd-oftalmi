from django.utils import timezone

from apps.audit.models import AuditAction
from apps.audit.services import audit_event_create_if_requested

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
    audit_context=None,
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
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.REQUEST_REGISTERED,
        module="document_requests",
        instance=document_request,
        description="Document request registered.",
        after_data={
            "request_type": document_request.request_type,
            "status": document_request.status,
            "title": document_request.title,
        },
    )
    return document_request


def document_request_transition_status(
    *,
    document_request,
    target_status,
    changed_at=None,
    audit_context=None,
):
    previous_status = document_request.status
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
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.OTHER,
        module="document_requests",
        instance=document_request,
        description="Document request status changed.",
        before_data={"status": previous_status},
        after_data={"status": document_request.status},
    )
    return document_request
