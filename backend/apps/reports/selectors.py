from apps.controlled_copies.models import ControlledCopyStatus
from apps.controlled_copies.selectors import controlled_copy_list
from apps.documents.models import DocumentStatus
from apps.documents.selectors import document_list, document_version_list
from apps.implementation_records.models import ImplementationRecordStatus
from apps.implementation_records.selectors import implementation_record_list


def _apply_date_range(queryset, *, field_name, date_from=None, date_to=None):
    if date_from is not None and date_to is not None and date_from > date_to:
        return queryset.none()

    if date_from is not None:
        queryset = queryset.filter(**{f"{field_name}__gte": date_from})
    if date_to is not None:
        queryset = queryset.filter(**{f"{field_name}__lte": date_to})

    return queryset


def _apply_status_group_filter(queryset, *, vigency=None, groups=None):
    if vigency in (None, "", "all"):
        return queryset

    statuses = (groups or {}).get(vigency)
    if statuses is None:
        return queryset

    return queryset.filter(status__in=statuses)


def get_master_book_queryset(
    *,
    document_type=None,
    organizational_unit=None,
    status=None,
    code=None,
    title=None,
    version_number=None,
    responsible_user=None,
    date_field="created_at",
    date_from=None,
    date_to=None,
    vigency=None,
):
    queryset = document_list().select_related("current_version__created_by")

    if document_type is not None:
        queryset = queryset.filter(document_type=document_type)
    if organizational_unit is not None:
        queryset = queryset.filter(owner_unit=organizational_unit)
    if status is not None:
        queryset = queryset.filter(status=status)
    if code is not None:
        queryset = queryset.filter(code=code)
    if title is not None:
        queryset = queryset.filter(title__icontains=title)
    if version_number is not None:
        queryset = queryset.filter(current_version__version_number=version_number)
    if responsible_user is not None:
        queryset = queryset.filter(created_by=responsible_user)

    queryset = _apply_status_group_filter(
        queryset,
        vigency=vigency,
        groups={
            "current": {DocumentStatus.PUBLISHED, DocumentStatus.ACTIVE},
            "draft": {DocumentStatus.DRAFT},
            "received": {DocumentStatus.RECEIVED},
            "under_review": {DocumentStatus.UNDER_REVIEW},
            "observed": {DocumentStatus.OBSERVED},
            "approved": {DocumentStatus.APPROVED},
            "published": {DocumentStatus.PUBLISHED},
            "active": {DocumentStatus.ACTIVE},
            "expired": {DocumentStatus.EXPIRED},
            "obsolete": {DocumentStatus.OBSOLETE},
            "archived": {DocumentStatus.ARCHIVED},
        },
    )
    return _apply_date_range(
        queryset,
        field_name=date_field,
        date_from=date_from,
        date_to=date_to,
    )


def get_monthly_document_report_queryset(
    *,
    document_type=None,
    organizational_unit=None,
    status=None,
    code=None,
    version_number=None,
    responsible_user=None,
    date_field="published_at",
    date_from=None,
    date_to=None,
    vigency=None,
):
    queryset = document_version_list().select_related(
        "document__document_type",
        "document__owner_unit",
        "document__current_version",
        "document__created_by",
        "created_by",
    )

    if document_type is not None:
        queryset = queryset.filter(document__document_type=document_type)
    if organizational_unit is not None:
        queryset = queryset.filter(document__owner_unit=organizational_unit)
    if status is not None:
        queryset = queryset.filter(status=status)
    if code is not None:
        queryset = queryset.filter(document__code=code)
    if version_number is not None:
        queryset = queryset.filter(version_number=version_number)
    if responsible_user is not None:
        queryset = queryset.filter(created_by=responsible_user)

    queryset = _apply_status_group_filter(
        queryset,
        vigency=vigency,
        groups={
            "current": {DocumentStatus.PUBLISHED, DocumentStatus.ACTIVE},
            "draft": {DocumentStatus.DRAFT},
            "received": {DocumentStatus.RECEIVED},
            "under_review": {DocumentStatus.UNDER_REVIEW},
            "observed": {DocumentStatus.OBSERVED},
            "approved": {DocumentStatus.APPROVED},
            "published": {DocumentStatus.PUBLISHED},
            "active": {DocumentStatus.ACTIVE},
            "expired": {DocumentStatus.EXPIRED},
            "obsolete": {DocumentStatus.OBSOLETE},
            "archived": {DocumentStatus.ARCHIVED},
        },
    )
    return _apply_date_range(
        queryset,
        field_name=date_field,
        date_from=date_from,
        date_to=date_to,
    )


def get_controlled_copies_report_queryset(
    *,
    document_type=None,
    organizational_unit=None,
    status=None,
    code=None,
    version_number=None,
    receiver_unit=None,
    receiver_user=None,
    responsible_user=None,
    date_field="delivered_at",
    date_from=None,
    date_to=None,
    vigency=None,
):
    queryset = controlled_copy_list().select_related(
        "document__document_type",
        "document__owner_unit",
        "document_version__created_by",
        "receiver_unit",
        "receiver_user",
        "created_by",
    )

    if document_type is not None:
        queryset = queryset.filter(document__document_type=document_type)
    if organizational_unit is not None:
        queryset = queryset.filter(document__owner_unit=organizational_unit)
    if status is not None:
        queryset = queryset.filter(status=status)
    if code is not None:
        queryset = queryset.filter(document__code=code)
    if version_number is not None:
        queryset = queryset.filter(document_version__version_number=version_number)
    if receiver_unit is not None:
        queryset = queryset.filter(receiver_unit=receiver_unit)
    if receiver_user is not None:
        queryset = queryset.filter(receiver_user=receiver_user)
    if responsible_user is not None:
        queryset = queryset.filter(created_by=responsible_user)

    queryset = _apply_status_group_filter(
        queryset,
        vigency=vigency,
        groups={
            "current": {
                ControlledCopyStatus.ACTIVE,
                ControlledCopyStatus.DELIVERED,
            },
            "registered": {ControlledCopyStatus.REGISTERED},
            "delivered": {ControlledCopyStatus.DELIVERED},
            "active": {ControlledCopyStatus.ACTIVE},
            "retired": {ControlledCopyStatus.RETIRED},
            "cancelled": {ControlledCopyStatus.CANCELLED},
        },
    )
    return _apply_date_range(
        queryset,
        field_name=date_field,
        date_from=date_from,
        date_to=date_to,
    )


def get_implementation_records_report_queryset(
    *,
    document_type=None,
    organizational_unit=None,
    status=None,
    code=None,
    version_number=None,
    user=None,
    responsible_user=None,
    date_field="assigned_at",
    date_from=None,
    date_to=None,
    vigency=None,
):
    queryset = implementation_record_list().select_related(
        "document__document_type",
        "document__owner_unit",
        "document_version__created_by",
    )

    effective_user = responsible_user if responsible_user is not None else user
    if effective_user is not None:
        queryset = queryset.filter(user=effective_user)
    if document_type is not None:
        queryset = queryset.filter(document__document_type=document_type)
    if organizational_unit is not None:
        queryset = queryset.filter(document__owner_unit=organizational_unit)
    if status is not None:
        queryset = queryset.filter(status=status)
    if code is not None:
        queryset = queryset.filter(document__code=code)
    if version_number is not None:
        queryset = queryset.filter(document_version__version_number=version_number)

    queryset = _apply_status_group_filter(
        queryset,
        vigency=vigency,
        groups={
            "current": {
                ImplementationRecordStatus.PENDING,
                ImplementationRecordStatus.READ,
                ImplementationRecordStatus.INTERPRETED,
                ImplementationRecordStatus.ACCEPTED,
                ImplementationRecordStatus.IMPLEMENTED,
            },
            "pending": {ImplementationRecordStatus.PENDING},
            "read": {ImplementationRecordStatus.READ},
            "interpreted": {ImplementationRecordStatus.INTERPRETED},
            "accepted": {ImplementationRecordStatus.ACCEPTED},
            "implemented": {ImplementationRecordStatus.IMPLEMENTED},
            "expired": {ImplementationRecordStatus.EXPIRED},
            "cancelled": {ImplementationRecordStatus.CANCELLED},
        },
    )
    return _apply_date_range(
        queryset,
        field_name=date_field,
        date_from=date_from,
        date_to=date_to,
    )
