from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentVersion
from apps.implementation_records.models import (
    ImplementationRecord,
    ImplementationRecordStatus,
)
from apps.organizational_units.models import OrganizationalUnit


class ImplementationRecordViewsTests(TestCase):
    def create_user(self, role, prefix):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
        )

    def create_record(self, *, user, document_version=None, status=None):
        return ImplementationRecord.objects.create(
            user=user,
            document=self.document,
            document_version=document_version or self.document_version,
            status=status or ImplementationRecordStatus.PENDING,
        )

    def setUp(self):
        self.oym_admin = self.create_user(UserRole.OYM_ADMIN, "oym-admin")
        self.reader = self.create_user(UserRole.READER, "reader")
        self.other_reader = self.create_user(UserRole.READER, "other-reader")
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.document = Document.objects.create(
            code="FOR-OYM-001",
            title="Documento para implementacion",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
        )
        self.document_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="01",
            created_by=self.oym_admin,
        )
        self.other_document_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="02",
            created_by=self.oym_admin,
        )
        self.reader_record = self.create_record(user=self.reader)
        self.other_record = self.create_record(
            user=self.other_reader,
            document_version=self.other_document_version,
            status=ImplementationRecordStatus.IMPLEMENTED,
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:implementation_records:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_oym_can_view_all_implementation_records(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(reverse("app:implementation_records:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "reader@oftalmi.test")
        self.assertContains(response, "other-reader@oftalmi.test")
        self.assertContains(response, "Nuevo registro propio")

    def test_user_can_view_only_own_implementation_records(self):
        self.client.force_login(self.reader)

        response = self.client.get(reverse("app:implementation_records:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "reader@oftalmi.test")
        self.assertNotContains(response, "other-reader@oftalmi.test")

    def test_user_can_view_own_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:implementation_records:detail", args=[self.reader_record.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001 v01")
        self.assertContains(response, "reader@oftalmi.test")

    def test_user_cannot_view_other_user_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:implementation_records:detail", args=[self.other_record.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_create_requires_login(self):
        response = self.client.get(reverse("app:implementation_records:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_user_can_create_own_pending_implementation_record(self):
        self.client.force_login(self.reader)

        response = self.client.post(
            reverse("app:implementation_records:create"),
            {
                "document": self.document.pk,
                "document_version": self.other_document_version.pk,
            },
        )

        created_record = ImplementationRecord.objects.get(
            user=self.reader,
            document_version=self.other_document_version,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("app:implementation_records:detail", args=[created_record.pk]),
        )
        self.assertEqual(created_record.document, self.document)
        self.assertEqual(created_record.status, ImplementationRecordStatus.PENDING)
        self.assertIsNone(created_record.read_at)
        self.assertIsNone(created_record.accepted_at)
        self.assertIsNone(created_record.implemented_at)

    def test_create_rejects_duplicate_user_document_version_record(self):
        self.client.force_login(self.reader)

        response = self.client.post(
            reverse("app:implementation_records:create"),
            {
                "document": self.document.pk,
                "document_version": self.document_version.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Ya existe un registro de implementacion propio para esta version.",
        )

    def test_create_rejects_version_from_another_document(self):
        other_document = Document.objects.create(
            code="FOR-OYM-002",
            title="Documento distinto",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
        )
        self.client.force_login(self.reader)

        response = self.client.post(
            reverse("app:implementation_records:create"),
            {
                "document": other_document.pk,
                "document_version": self.document_version.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "La version documental debe pertenecer al documento seleccionado.",
        )
