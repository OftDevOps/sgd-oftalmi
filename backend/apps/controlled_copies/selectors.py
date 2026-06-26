from .models import ControlledCopy, ControlledCopyStatus


def controlled_copy_list(
    *,
    document=None,
    document_version=None,
    receiver_unit=None,
    receiver_user=None,
    status=None,
):
    queryset = ControlledCopy.objects.select_related(
        "document",
        "document_version",
        "receiver_unit",
        "receiver_user",
        "created_by",
    )

    if document is not None:
        queryset = queryset.filter(document=document)
    if document_version is not None:
        queryset = queryset.filter(document_version=document_version)
    if receiver_unit is not None:
        queryset = queryset.filter(receiver_unit=receiver_unit)
    if receiver_user is not None:
        queryset = queryset.filter(receiver_user=receiver_user)
    if status is not None:
        queryset = queryset.filter(status=status)

    return queryset


def active_controlled_copy_list():
    return controlled_copy_list(status=ControlledCopyStatus.ACTIVE)


def retired_controlled_copy_list():
    return controlled_copy_list(status=ControlledCopyStatus.RETIRED)
