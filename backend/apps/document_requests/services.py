from .models import DocumentRequest


def document_request_create(
    *,
    request_type,
    title,
    requested_by,
    organizational_unit,
    description="",
    document_type=None,
    related_document=None,
    status=None,
    submitted_at=None,
    closed_at=None,
):
    document_request = DocumentRequest(
        request_type=request_type,
        title=title,
        description=description,
        requested_by=requested_by,
        organizational_unit=organizational_unit,
        document_type=document_type,
        related_document=related_document,
        submitted_at=submitted_at,
        closed_at=closed_at,
    )
    if status is not None:
        document_request.status = status

    document_request.full_clean()
    document_request.save()
    return document_request
