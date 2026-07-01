from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentFile, DocumentStatus, DocumentVersion
from apps.organizational_units.models import OrganizationalUnit


class DocumentViewsTests(TestCase):
    def create_user(self, role, prefix):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
        )

    def setUp(self):
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.oym_admin = self.create_user(UserRole.OYM_ADMIN, "oym_admin")
        self.oym_analyst = self.create_user(UserRole.OYM_ANALYST, "oym_analyst")
        self.executing_unit = self.create_user(UserRole.EXECUTING_UNIT, "executing_unit")
        self.reader = self.create_user(UserRole.READER, "reader")
        self.systems_admin = self.create_user(UserRole.SYSTEMS_TECH_ADMIN, "systems_admin")

        self.active_document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro de Recepcion de Informacion",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.ACTIVE,
        )
        self.active_version = DocumentVersion.objects.create(
            document=self.active_document,
            version_number="01",
            status=DocumentStatus.PUBLISHED,
            created_by=self.oym_admin,
        )
        self.active_document.current_version = self.active_version
        self.active_document.save(update_fields=["current_version", "updated_at"])

        DocumentFile.objects.create(
            document_version=self.active_version,
            file="documents/2026/07/for-oym-001-v01.pdf",
            original_filename="for-oym-001-v01.pdf",
            content_type="application/pdf",
            size_bytes=2048,
            file_hash="hash-v01",
            uploaded_by=self.oym_admin,
        )

        self.draft_version = DocumentVersion.objects.create(
            document=self.active_document,
            version_number="02",
            status=DocumentStatus.DRAFT,
            created_by=self.oym_admin,
        )
        DocumentFile.objects.create(
            document_version=self.draft_version,
            file="documents/2026/07/for-oym-001-v02.pdf",
            original_filename="for-oym-001-v02.pdf",
            content_type="application/pdf",
            size_bytes=3072,
            file_hash="hash-v02",
            uploaded_by=self.oym_admin,
        )

        self.obsolete_document = Document.objects.create(
            code="FOR-OYM-009",
            title="Documento obsoleto",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.OBSOLETE,
        )
        self.obsolete_version = DocumentVersion.objects.create(
            document=self.obsolete_document,
            version_number="01",
            status=DocumentStatus.OBSOLETE,
            created_by=self.oym_admin,
        )
        self.obsolete_document.current_version = self.obsolete_version
        self.obsolete_document.save(update_fields=["current_version", "updated_at"])

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:documents:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_allowed_roles_can_view_visible_documents(self):
        allowed_roles = (
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        )

        for role in allowed_roles:
            with self.subTest(role=role):
                self.client.logout()
                self.client.force_login(self.create_user(role, f"allowed-{role}"))

                response = self.client.get(reverse("app:documents:index"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Documentos")
                self.assertContains(response, "FOR-OYM-001")
                if role in (UserRole.OYM_ADMIN, UserRole.OYM_ANALYST):
                    self.assertContains(response, "FOR-OYM-009")
                else:
                    self.assertNotContains(response, "FOR-OYM-009")

    def test_disallowed_role_cannot_view_list(self):
        self.client.force_login(self.systems_admin)

        response = self.client.get(reverse("app:documents:index"))

        self.assertEqual(response.status_code, 403)

    def test_oym_can_view_detail_with_versions_and_file_metadata(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.active_document.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001 - Registro de Recepcion de Informacion")
        self.assertContains(response, "01")
        self.assertContains(response, "02")
        self.assertContains(response, "for-oym-001-v01.pdf")
        self.assertContains(response, "for-oym-001-v02.pdf")
        self.assertContains(response, "hash-v01")
        self.assertContains(response, "hash-v02")

    def test_reader_sees_only_visible_versions_in_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.active_document.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001 - Registro de Recepcion de Informacion")
        self.assertContains(response, "01")
        self.assertContains(response, "for-oym-001-v01.pdf")
        self.assertNotContains(response, "for-oym-001-v02.pdf")
        self.assertNotContains(response, "hash-v02")

    def test_reader_cannot_view_obsolete_document_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.obsolete_document.pk])
        )

        self.assertEqual(response.status_code, 404)
