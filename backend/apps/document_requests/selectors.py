from .models import DocumentRequest


def document_request_list(
    *,
    request_type=None,
    status=None,
    requested_by=None,
    organizational_unit=None,
    document_type=None,
    related_document=None,
):
    queryset = DocumentRequest.objects.select_related(
        "requested_by",
        "organizational_unit",
        "document_type",
        "related_document",
    )

    if request_type is not None:
        queryset = queryset.filter(request_type=request_type)
    if status is not None:
        queryset = queryset.filter(status=status)
    if requested_by is not None:
        queryset = queryset.filter(requested_by=requested_by)
    if organizational_unit is not None:
        queryset = queryset.filter(organizational_unit=organizational_unit)
    if document_type is not None:
        queryset = queryset.filter(document_type=document_type)
    if related_document is not None:
        queryset = queryset.filter(related_document=related_document)

    return queryset


def document_request_get_for_user(*, user, document_request_id):
    return document_request_list(requested_by=user).filter(id=document_request_id).first()
