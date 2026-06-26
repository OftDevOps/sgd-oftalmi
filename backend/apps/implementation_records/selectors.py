from .models import ImplementationRecord, ImplementationRecordStatus


def implementation_record_list(
    *,
    user=None,
    document=None,
    document_version=None,
    status=None,
):
    queryset = ImplementationRecord.objects.select_related(
        "user",
        "document",
        "document_version",
    )

    if user is not None:
        queryset = queryset.filter(user=user)
    if document is not None:
        queryset = queryset.filter(document=document)
    if document_version is not None:
        queryset = queryset.filter(document_version=document_version)
    if status is not None:
        queryset = queryset.filter(status=status)

    return queryset


def pending_implementation_record_list(*, user=None):
    return implementation_record_list(
        user=user,
        status=ImplementationRecordStatus.PENDING,
    )


def implemented_record_list(*, user=None):
    return implementation_record_list(
        user=user,
        status=ImplementationRecordStatus.IMPLEMENTED,
    )
