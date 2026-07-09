from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentStatus, DocumentVersion
from apps.organizational_units.models import OrganizationalUnit


class MasterBookViewTests(TestCase):
    def create_user(self, role, prefix):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
        )

    def setUp(self):
        self.oym_admin = self.create_user(UserRole.OYM_ADMIN, "oym-admin")
        self.oym_analyst = self.create_user(UserRole.OYM_ANALYST, "oym-analyst")
        self.reader = self.create_user(UserRole.READER, "reader")
        self.executing_unit = self.create_user(UserRole.EXECUTING_UNIT, "executing-unit")
        self.systems_user = self.create_user(UserRole.SYSTEMS_TECH_ADMIN, "systems")
        self.auditor = self.create_user(UserRole.AUDITOR, "auditor")

        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        self.document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro principal",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.ACTIVE,
        )
        self.version = DocumentVersion.objects.create(
            document=self.document,
            version_number="01",
            status=DocumentStatus.ACTIVE,
            issue_date=date(2026, 1, 10),
            effective_date=date(2026, 1, 15),
            created_by=self.oym_admin,
        )
        Document.objects.filter(pk=self.document.pk).update(
            current_version_id=self.version.pk,
        )

    def test_master_book_requires_login(self):
        response = self.client.get(reverse("app:reports:master_book"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_oym_roles_can_view_master_book(self):
        for user in (self.oym_admin, self.oym_analyst):
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:reports:master_book"))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "reports/master_book.html")
                self.assertContains(response, "Libro Maestro documental")

    def test_disallowed_roles_cannot_view_master_book(self):
        denied_users = (
            self.reader,
            self.executing_unit,
            self.systems_user,
            self.auditor,
        )

        for user in denied_users:
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:reports:master_book"))

                self.assertEqual(response.status_code, 403)

    def test_master_book_renders_document_rows(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(reverse("app:reports:master_book"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertContains(response, "Registro principal")
        self.assertContains(response, "FOR - Formato")
        self.assertContains(response, "OyM")
        self.assertContains(response, "Active")
        self.assertContains(response, "01")
        self.assertContains(response, "2026-01-10")
        self.assertContains(response, "2026-01-15")
        self.assertNotContains(response, "/media/")

    def test_master_book_view_uses_report_selector(self):
        self.client.force_login(self.oym_admin)

        with patch(
            "apps.reports.views.get_master_book_queryset",
            return_value=Document.objects.none(),
        ) as selector:
            response = self.client.get(reverse("app:reports:master_book"))

        self.assertEqual(response.status_code, 200)
        selector.assert_called_once_with()
