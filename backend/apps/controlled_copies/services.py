from .models import ControlledCopy


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
    return controlled_copy
