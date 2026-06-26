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
    return implementation_record
