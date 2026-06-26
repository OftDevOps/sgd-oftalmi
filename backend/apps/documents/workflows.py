from django.core.exceptions import ValidationError

from .models import DocumentStatus


DOCUMENT_STATUS_TRANSITIONS = {
    DocumentStatus.DRAFT: {
        DocumentStatus.RECEIVED,
        DocumentStatus.UNDER_REVIEW,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.RECEIVED: {
        DocumentStatus.UNDER_REVIEW,
        DocumentStatus.OBSERVED,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.UNDER_REVIEW: {
        DocumentStatus.OBSERVED,
        DocumentStatus.APPROVED,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.OBSERVED: {
        DocumentStatus.UNDER_REVIEW,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.APPROVED: {
        DocumentStatus.PUBLISHED,
        DocumentStatus.ACTIVE,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.PUBLISHED: {
        DocumentStatus.ACTIVE,
        DocumentStatus.OBSOLETE,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.ACTIVE: {
        DocumentStatus.EXPIRED,
        DocumentStatus.OBSOLETE,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.EXPIRED: {
        DocumentStatus.OBSOLETE,
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.OBSOLETE: {
        DocumentStatus.ARCHIVED,
    },
    DocumentStatus.ARCHIVED: set(),
}


def get_allowed_document_status_transitions(status):
    return DOCUMENT_STATUS_TRANSITIONS.get(status, set())


def can_transition_document_status(current_status, target_status):
    if current_status == target_status:
        return True

    return target_status in get_allowed_document_status_transitions(current_status)


def validate_document_status_transition(current_status, target_status):
    if not can_transition_document_status(current_status, target_status):
        raise ValidationError(
            f"Document status transition from '{current_status}' to '{target_status}' is not allowed."
        )
