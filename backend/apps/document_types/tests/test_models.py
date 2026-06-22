from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.document_types.models import DocumentType


class DocumentTypeModelTests(TestCase):
    def test_create_document_type_with_code_and_name(self):
        document_type = DocumentType.objects.create(code="FOR", name="Formato")

        self.assertEqual(document_type.code, "FOR")
        self.assertEqual(document_type.name, "Formato")

    def test_string_representation(self):
        document_type = DocumentType.objects.create(code="DOC", name="Documento")

        self.assertEqual(str(document_type), "DOC - Documento")

    def test_is_active_defaults_to_true(self):
        document_type = DocumentType.objects.create(code="MAN", name="Manual")

        self.assertTrue(document_type.is_active)

    def test_code_is_unique(self):
        DocumentType.objects.create(code="PRO", name="Procedimiento")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DocumentType.objects.create(code="PRO", name="Proceso")
