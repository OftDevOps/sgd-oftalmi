from .models import DocumentType


def document_type_list(*, is_active=None):
    queryset = DocumentType.objects.all()

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def document_type_get_by_code(code):
    if not code:
        return None

    return DocumentType.objects.filter(code=code).first()
