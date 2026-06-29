from apps.audit.models import AuditAction
from apps.audit.services import audit_event_create_if_requested

from .models import ImplementationRecord


def implementation_record_create(
    *,
    user,
    document,
    document_version,
    assigned_at=None,
    read_at=None,
    interpreted_at=None,
    accepted_at=None,
    implemented_at=None,
    status=None,
    audit_context=None,
):
    implementation_record = ImplementationRecord(
        user=user,
        document=document,
        document_version=document_version,
        read_at=read_at,
        interpreted_at=interpreted_at,
        accepted_at=accepted_at,
        implemented_at=implemented_at,
    )
    if assigned_at is not None:
        implementation_record.assigned_at = assigned_at
    if status is not None:
        implementation_record.status = status

    implementation_record.full_clean()
    implementation_record.save()
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.IMPLEMENTATION_RECORD_REGISTERED,
        module="implementation_records",
        instance=implementation_record,
        description="Implementation record registered.",
        after_data={
            "user_id": user.id,
            "document_id": document.id,
            "document_version_id": document_version.id,
            "status": implementation_record.status,
        },
    )
    return implementation_record
