from .models import DocumentType


def document_type_create(*, code, name, description="", is_active=True):
    document_type = DocumentType(
        code=code,
        name=name,
        description=description,
        is_active=is_active,
    )
    document_type.full_clean()
    document_type.save()
    return document_type
