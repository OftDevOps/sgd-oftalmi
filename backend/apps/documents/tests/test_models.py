from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentFile, DocumentStatus, DocumentVersion
from apps.organizational_units.models import OrganizationalUnit


class DocumentModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="oym@example.com",
            password="test-pass",
        )
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )

    def create_document(self, **kwargs):
        defaults = {
            "code": "FOR-GGHD-010",
            "title": "Registro de Recepcion de Informacion",
            "document_type": self.document_type,
            "owner_unit": self.owner_unit,
            "created_by": self.user,
        }
        defaults.update(kwargs)
        return Document.objects.create(**defaults)

    def test_create_document_with_required_catalog_relations(self):
        document = self.create_document()

        self.assertEqual(document.code, "FOR-GGHD-010")
        self.assertEqual(document.document_type, self.document_type)
        self.assertEqual(document.owner_unit, self.owner_unit)
        self.assertEqual(document.created_by, self.user)

    def test_document_defaults_to_draft_and_active(self):
        document = self.create_document()

        self.assertEqual(document.status, DocumentStatus.DRAFT)
        self.assertTrue(document.is_active)

    def test_document_string_representation(self):
        document = self.create_document()

        self.assertEqual(str(document), "FOR-GGHD-010 - Registro de Recepcion de Informacion")

    def test_document_code_is_unique(self):
        self.create_document()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_document(title="Duplicated code")

    def test_create_document_version(self):
        document = self.create_document()
        version = DocumentVersion.objects.create(
            document=document,
            version_number="01",
            created_by=self.user,
        )

        self.assertEqual(version.document, document)
        self.assertEqual(version.status, DocumentStatus.DRAFT)
        self.assertEqual(str(version), "FOR-GGHD-010 v01")

    def test_version_number_is_unique_per_document(self):
        document = self.create_document()
        DocumentVersion.objects.create(
            document=document,
            version_number="01",
            created_by=self.user,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DocumentVersion.objects.create(
                    document=document,
                    version_number="01",
                    created_by=self.user,
                )

    def test_document_can_reference_current_version(self):
        document = self.create_document()
        version = DocumentVersion.objects.create(
            document=document,
            version_number="01",
            status=DocumentStatus.ACTIVE,
            created_by=self.user,
        )

        document.current_version = version
        document.status = DocumentStatus.ACTIVE
        document.save(update_fields=["current_version", "status", "updated_at"])

        document.refresh_from_db()
        self.assertEqual(document.current_version, version)
        self.assertEqual(document.status, DocumentStatus.ACTIVE)

    def test_create_document_file_with_traceability_metadata(self):
        document = self.create_document()
        version = DocumentVersion.objects.create(
            document=document,
            version_number="01",
            created_by=self.user,
        )
        document_file = DocumentFile.objects.create(
            document_version=version,
            file="documents/2026/06/for-gghd-010.pdf",
            original_filename="for-gghd-010.pdf",
            content_type="application/pdf",
            size_bytes=1024,
            file_hash="abc123",
            uploaded_by=self.user,
        )

        self.assertEqual(document_file.document_version, version)
        self.assertEqual(document_file.uploaded_by, self.user)
        self.assertTrue(document_file.is_active)
        self.assertEqual(str(document_file), "for-gghd-010.pdf")
