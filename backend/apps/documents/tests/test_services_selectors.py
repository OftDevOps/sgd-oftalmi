from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.document_types.models import DocumentType
from apps.documents.models import DocumentStatus
from apps.documents.selectors import document_get_by_code, document_list, document_version_list
from apps.documents.services import (
    document_create,
    document_set_current_version,
    document_version_create,
)
from apps.organizational_units.models import OrganizationalUnit


class DocumentServicesSelectorsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="oym@oftalmi.com",
            password="test-pass",
        )
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )

    def test_create_document_version_and_selectors(self):
        document = document_create(
            code="FOR-OYM-001",
            title="Registro base",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.user,
        )
        version = document_version_create(
            document=document,
            version_number="01",
            created_by=self.user,
            status=DocumentStatus.ACTIVE,
        )
        document_set_current_version(document=document, document_version=version)

        document.refresh_from_db()
        self.assertEqual(document.current_version, version)
        self.assertEqual(document_get_by_code("FOR-OYM-001"), document)
        self.assertEqual(list(document_list(owner_unit=self.owner_unit)), [document])
        self.assertEqual(list(document_version_list(status=DocumentStatus.ACTIVE)), [version])
