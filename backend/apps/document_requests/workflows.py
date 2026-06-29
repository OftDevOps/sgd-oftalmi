from django.core.exceptions import ValidationError

from .models import DocumentRequestStatus


DOCUMENT_REQUEST_STATUS_TRANSITIONS = {
    DocumentRequestStatus.DRAFT: {
        DocumentRequestStatus.SUBMITTED,
        DocumentRequestStatus.CANCELLED,
    },
    DocumentRequestStatus.SUBMITTED: {
        DocumentRequestStatus.RECEIVED,
        DocumentRequestStatus.OBSERVED,
        DocumentRequestStatus.CANCELLED,
    },
    DocumentRequestStatus.RECEIVED: {
        DocumentRequestStatus.IN_REVIEW,
        DocumentRequestStatus.OBSERVED,
        DocumentRequestStatus.CANCELLED,
    },
    DocumentRequestStatus.IN_REVIEW: {
        DocumentRequestStatus.OBSERVED,
        DocumentRequestStatus.CLOSED,
        DocumentRequestStatus.CANCELLED,
    },
    DocumentRequestStatus.OBSERVED: {
        DocumentRequestStatus.SUBMITTED,
        DocumentRequestStatus.RECEIVED,
        DocumentRequestStatus.CANCELLED,
    },
    DocumentRequestStatus.CANCELLED: set(),
    DocumentRequestStatus.CLOSED: set(),
}


def get_allowed_document_request_status_transitions(status):
    return DOCUMENT_REQUEST_STATUS_TRANSITIONS.get(status, set())


def can_transition_document_request_status(current_status, target_status):
    if current_status == target_status:
        return True

    return target_status in get_allowed_document_request_status_transitions(current_status)


def validate_document_request_status_transition(current_status, target_status):
    if not can_transition_document_request_status(current_status, target_status):
        raise ValidationError(
            (
                "Document request status transition from "
                f"'{current_status}' to '{target_status}' is not allowed."
            )
        )
