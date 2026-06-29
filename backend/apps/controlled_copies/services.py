from django.utils import timezone

from apps.audit.models import AuditAction
from apps.audit.services import audit_event_create_if_requested

from .models import ControlledCopy, ControlledCopyStatus


def controlled_copy_create(
    *,
    document,
    document_version,
    copy_number,
    receiver_unit,
    created_by,
    receiver_user=None,
    delivered_at=None,
    retired_at=None,
    status=None,
    observations="",
    evidence_reference="",
    audit_context=None,
):
    controlled_copy = ControlledCopy(
        document=document,
        document_version=document_version,
        copy_number=copy_number,
        receiver_unit=receiver_unit,
        receiver_user=receiver_user,
        delivered_at=delivered_at,
        retired_at=retired_at,
        observations=observations,
        evidence_reference=evidence_reference,
        created_by=created_by,
    )
    if status is not None:
        controlled_copy.status = status

    controlled_copy.full_clean()
    controlled_copy.save()
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.OTHER,
        module="controlled_copies",
        instance=controlled_copy,
        description="Controlled copy registered.",
        after_data={
            "document_id": document.id,
            "document_version_id": document_version.id,
            "copy_number": copy_number,
            "status": controlled_copy.status,
        },
    )
    return controlled_copy


def controlled_copy_register_delivery(
    *,
    controlled_copy,
    delivered_at=None,
    audit_context=None,
):
    delivered_at = delivered_at or timezone.now()
    previous_status = controlled_copy.status

    controlled_copy.status = ControlledCopyStatus.DELIVERED
    controlled_copy.delivered_at = delivered_at
    controlled_copy.full_clean()
    controlled_copy.save(update_fields=["status", "delivered_at", "updated_at"])
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.CONTROLLED_COPY_DELIVERED,
        module="controlled_copies",
        instance=controlled_copy,
        description="Controlled copy delivered.",
        before_data={"status": previous_status},
        after_data={
            "status": controlled_copy.status,
            "delivered_at": delivered_at.isoformat(),
        },
    )
    return controlled_copy


def controlled_copy_register_retirement(
    *,
    controlled_copy,
    retired_at=None,
    audit_context=None,
):
    retired_at = retired_at or timezone.now()
    previous_status = controlled_copy.status

    controlled_copy.status = ControlledCopyStatus.RETIRED
    controlled_copy.retired_at = retired_at
    controlled_copy.full_clean()
    controlled_copy.save(update_fields=["status", "retired_at", "updated_at"])
    audit_event_create_if_requested(
        audit_context=audit_context,
        action=AuditAction.CONTROLLED_COPY_RETIRED,
        module="controlled_copies",
        instance=controlled_copy,
        description="Controlled copy retired.",
        before_data={"status": previous_status},
        after_data={
            "status": controlled_copy.status,
            "retired_at": retired_at.isoformat(),
        },
    )
    return controlled_copy
