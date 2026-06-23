from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.document_requests.models import (
    DocumentRequest,
    DocumentRequestStatus,
    DocumentRequestType,
)
from apps.document_types.models import DocumentType
from apps.documents.models import Document
from apps.organizational_units.models import OrganizationalUnit


class DocumentRequestModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="solicitante@example.com",
            password="test-pass",
        )
        self.organizational_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.document_type = DocumentType.objects.create(
            code="FOR",
            name="Formato",
        )

    def create_document(self, **kwargs):
        defaults = {
            "code": "FOR-OYM-001",
            "title": "Registro de Solicitud Documental",
            "document_type": self.document_type,
            "owner_unit": self.organizational_unit,
            "created_by": self.user,
        }
        defaults.update(kwargs)
        return Document.objects.create(**defaults)

    def create_document_request(self, **kwargs):
        defaults = {
            "request_type": DocumentRequestType.CREATE,
            "title": "Solicitud de creacion documental",
            "requested_by": self.user,
            "organizational_unit": self.organizational_unit,
        }
        defaults.update(kwargs)
        return DocumentRequest.objects.create(**defaults)

    def test_create_minimal_valid_document_request(self):
        document_request = self.create_document_request()

        self.assertEqual(document_request.request_type, DocumentRequestType.CREATE)
        self.assertEqual(document_request.title, "Solicitud de creacion documental")
        self.assertEqual(document_request.requested_by, self.user)
        self.assertEqual(document_request.organizational_unit, self.organizational_unit)

    def test_document_request_defaults_to_draft_status(self):
        document_request = self.create_document_request()

        self.assertEqual(document_request.status, DocumentRequestStatus.DRAFT)

    def test_document_request_string_representation(self):
        document_request = self.create_document_request()

        self.assertEqual(str(document_request), "Creation - Solicitud de creacion documental")

    def test_create_document_request_related_to_existing_document(self):
        document = self.create_document()
        document_request = self.create_document_request(
            request_type=DocumentRequestType.MODIFY,
            related_document=document,
        )

        self.assertEqual(document_request.related_document, document)

    def test_create_document_request_with_document_type(self):
        document_request = self.create_document_request(document_type=self.document_type)

        self.assertEqual(document_request.document_type, self.document_type)

    def test_document_request_keeps_requested_by_relation(self):
        document_request = self.create_document_request()

        self.assertEqual(document_request.requested_by, self.user)
        self.assertIn(document_request, self.user.document_requests.all())

    def test_document_request_keeps_organizational_unit_relation(self):
        document_request = self.create_document_request()

        self.assertEqual(document_request.organizational_unit, self.organizational_unit)
        self.assertIn(document_request, self.organizational_unit.document_requests.all())

    def test_document_type_is_optional(self):
        document_request = self.create_document_request()

        self.assertIsNone(document_request.document_type)

    def test_related_document_is_optional(self):
        document_request = self.create_document_request()

        self.assertIsNone(document_request.related_document)

    def test_can_create_document_request_for_each_defined_type(self):
        for index, request_type in enumerate(DocumentRequestType.values, start=1):
            with self.subTest(request_type=request_type):
                document_request = self.create_document_request(
                    request_type=request_type,
                    title=f"Solicitud documental {index}",
                )

                self.assertEqual(document_request.request_type, request_type)
