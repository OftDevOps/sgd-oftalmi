from .models import Document, DocumentFile, DocumentVersion


def document_list(*, status=None, is_active=None, owner_unit=None, document_type=None):
    queryset = Document.objects.select_related(
        "document_type",
        "owner_unit",
        "current_version",
        "created_by",
    )

    if status is not None:
        queryset = queryset.filter(status=status)
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    if owner_unit is not None:
        queryset = queryset.filter(owner_unit=owner_unit)
    if document_type is not None:
        queryset = queryset.filter(document_type=document_type)

    return queryset


def document_get_by_code(code):
    if not code:
        return None

    return document_list().filter(code=code).first()


def document_version_list(*, document=None, status=None):
    queryset = DocumentVersion.objects.select_related("document", "created_by")

    if document is not None:
        queryset = queryset.filter(document=document)
    if status is not None:
        queryset = queryset.filter(status=status)

    return queryset


def document_file_list(*, document_version=None, is_active=None):
    queryset = DocumentFile.objects.select_related("document_version", "uploaded_by")

    if document_version is not None:
        queryset = queryset.filter(document_version=document_version)
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def document_detail_queryset():
    return document_list().prefetch_related("versions__created_by", "versions__files__uploaded_by")
