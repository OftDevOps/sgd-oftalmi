from datetime import date, datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import UserRole
from apps.controlled_copies.models import ControlledCopy, ControlledCopyStatus
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
        self.other_document_type = DocumentType.objects.create(
            code="PRO",
            name="Procedimiento",
        )
        self.owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        self.other_owner_unit = OrganizationalUnit.objects.create(
            name="Administracion",
            code="ADM",
        )
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
        self.other_document = Document.objects.create(
            code="PRO-ADM-001",
            title="Procedimiento administrativo",
            document_type=self.other_document_type,
            owner_unit=self.other_owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.DRAFT,
        )
        self.other_version = DocumentVersion.objects.create(
            document=self.other_document,
            version_number="B",
            status=DocumentStatus.DRAFT,
            issue_date=date(2026, 2, 10),
            effective_date=date(2026, 2, 15),
            created_by=self.oym_admin,
        )
        Document.objects.filter(pk=self.other_document.pk).update(
            current_version_id=self.other_version.pk,
        )
        self.monthly_document = Document.objects.create(
            code="MEN-OYM-001",
            title="Actividad mensual publicada",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.PUBLISHED,
        )
        self.monthly_version = DocumentVersion.objects.create(
            document=self.monthly_document,
            version_number="03",
            status=DocumentStatus.PUBLISHED,
            issue_date=date(2026, 7, 5),
            effective_date=date(2026, 7, 8),
            published_at=timezone.make_aware(datetime(2026, 7, 9, 10, 30)),
            created_by=self.oym_admin,
        )
        Document.objects.filter(pk=self.monthly_document.pk).update(
            current_version_id=self.monthly_version.pk,
        )
        self.monthly_active_document = Document.objects.create(
            code="MEN-ADM-001",
            title="Actividad mensual activa",
            document_type=self.other_document_type,
            owner_unit=self.other_owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.ACTIVE,
        )
        self.monthly_active_version = DocumentVersion.objects.create(
            document=self.monthly_active_document,
            version_number="01",
            status=DocumentStatus.ACTIVE,
            issue_date=date(2026, 7, 12),
            effective_date=date(2026, 7, 15),
            published_at=timezone.make_aware(datetime(2026, 7, 16, 9, 0)),
            created_by=self.oym_admin,
        )
        Document.objects.filter(pk=self.monthly_active_document.pk).update(
            current_version_id=self.monthly_active_version.pk,
        )
        self.other_month_document = Document.objects.create(
            code="MEN-OYM-002",
            title="Actividad de otro mes",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.PUBLISHED,
        )
        self.other_month_version = DocumentVersion.objects.create(
            document=self.other_month_document,
            version_number="01",
            status=DocumentStatus.PUBLISHED,
            issue_date=date(2026, 8, 5),
            effective_date=date(2026, 8, 8),
            published_at=timezone.make_aware(datetime(2026, 8, 9, 10, 30)),
            created_by=self.oym_admin,
        )
        Document.objects.filter(pk=self.other_month_document.pk).update(
            current_version_id=self.other_month_version.pk,
        )
        self.controlled_copy = ControlledCopy.objects.create(
            document=self.document,
            document_version=self.version,
            copy_number="CC-001",
            receiver_unit=self.other_owner_unit,
            receiver_user=self.reader,
            delivered_at=timezone.make_aware(datetime(2026, 7, 10, 8, 0)),
            status=ControlledCopyStatus.ACTIVE,
            created_by=self.oym_admin,
        )
        self.retired_controlled_copy = ControlledCopy.objects.create(
            document=self.other_document,
            document_version=self.other_version,
            copy_number="CC-002",
            receiver_unit=self.owner_unit,
            receiver_user=self.executing_unit,
            delivered_at=timezone.make_aware(datetime(2026, 6, 1, 8, 0)),
            retired_at=timezone.make_aware(datetime(2026, 6, 15, 17, 0)),
            status=ControlledCopyStatus.RETIRED,
            created_by=self.oym_admin,
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

    def test_master_book_filters_by_document_type(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {"document_type": self.document_type.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertNotContains(response, "PRO-ADM-001")

    def test_master_book_filters_by_owner_unit(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {"organizational_unit": self.other_owner_unit.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PRO-ADM-001")
        self.assertNotContains(response, "FOR-OYM-001")

    def test_master_book_filters_by_status(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {"status": DocumentStatus.ACTIVE},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertNotContains(response, "PRO-ADM-001")

    def test_master_book_filters_by_vigency_group(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {"vigency": "current"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertNotContains(response, "PRO-ADM-001")

    def test_master_book_filters_by_code_and_title(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {
                "code": "PRO-ADM-001",
                "title": "administrativo",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PRO-ADM-001")
        self.assertNotContains(response, "FOR-OYM-001")

    def test_invalid_filters_do_not_break_master_book(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {
                "document_type": "999999",
                "status": "invalid",
                "date_from": "not-a-date",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Libro Maestro documental")
        self.assertContains(response, "FOR-OYM-001")
        self.assertContains(response, "PRO-ADM-001")

    def test_selected_filters_are_kept_in_template(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:master_book"),
            {
                "document_type": self.document_type.pk,
                "organizational_unit": self.owner_unit.pk,
                "status": DocumentStatus.ACTIVE,
                "vigency": "current",
                "code": "FOR-OYM-001",
                "title": "Registro",
                "date_from": "2026-01-01",
                "date_to": "2026-12-31",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'<option value="{self.document_type.pk}" selected>',
            html=False,
        )
        self.assertContains(
            response,
            f'<option value="{self.owner_unit.pk}" selected>',
            html=False,
        )
        self.assertContains(response, '<option value="active" selected>', html=False)
        self.assertContains(response, '<option value="current" selected>', html=False)
        self.assertContains(response, 'value="FOR-OYM-001"', html=False)
        self.assertContains(response, 'value="Registro"', html=False)
        self.assertContains(response, 'value="2026-01-01"', html=False)
        self.assertContains(response, 'value="2026-12-31"', html=False)

    def test_master_book_view_uses_report_selector(self):
        self.client.force_login(self.oym_admin)

        with patch(
            "apps.reports.views.get_master_book_queryset",
            return_value=Document.objects.none(),
        ) as selector:
            response = self.client.get(reverse("app:reports:master_book"))

        self.assertEqual(response.status_code, 200)
        selector.assert_called_once_with()

    def test_master_book_view_passes_clean_filters_to_selector(self):
        self.client.force_login(self.oym_admin)

        with patch(
            "apps.reports.views.get_master_book_queryset",
            return_value=Document.objects.none(),
        ) as selector:
            response = self.client.get(
                reverse("app:reports:master_book"),
                {
                    "document_type": self.document_type.pk,
                    "organizational_unit": self.owner_unit.pk,
                    "status": DocumentStatus.ACTIVE,
                    "vigency": "current",
                    "code": "FOR-OYM-001",
                    "title": "Registro",
                    "date_from": "2026-01-01",
                    "date_to": "2026-12-31",
                },
            )

        self.assertEqual(response.status_code, 200)
        selector.assert_called_once_with(
            document_type=self.document_type,
            organizational_unit=self.owner_unit,
            status=DocumentStatus.ACTIVE,
            vigency="current",
            code="FOR-OYM-001",
            title="Registro",
            date_from=date(2026, 1, 1),
            date_to=date(2026, 12, 31),
            date_field="created_at__date",
        )

    def test_monthly_report_requires_login(self):
        response = self.client.get(reverse("app:reports:monthly_documents"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_oym_roles_can_view_monthly_report(self):
        for user in (self.oym_admin, self.oym_analyst):
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:reports:monthly_documents"))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "reports/monthly_documents.html")
                self.assertContains(response, "Reporte mensual documental")

    def test_disallowed_roles_cannot_view_monthly_report(self):
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

                response = self.client.get(reverse("app:reports:monthly_documents"))

                self.assertEqual(response.status_code, 403)

    def test_monthly_report_filters_by_month_and_year(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:monthly_documents"),
            {"month": "7", "year": "2026"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2026-07")
        self.assertContains(response, "MEN-OYM-001")
        self.assertContains(response, "MEN-ADM-001")
        self.assertNotContains(response, "MEN-OYM-002")
        self.assertEqual(response.context["report_summary"]["total"], 2)
        self.assertIn(("Active", 1), response.context["report_summary"]["status_totals"])
        self.assertIn(
            ("Published", 1),
            response.context["report_summary"]["status_totals"],
        )

    def test_monthly_report_filters_by_document_type(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:monthly_documents"),
            {
                "month": "7",
                "year": "2026",
                "document_type": self.document_type.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MEN-OYM-001")
        self.assertNotContains(response, "MEN-ADM-001")

    def test_monthly_report_filters_by_owner_unit(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:monthly_documents"),
            {
                "month": "7",
                "year": "2026",
                "organizational_unit": self.other_owner_unit.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MEN-ADM-001")
        self.assertNotContains(response, "MEN-OYM-001")

    def test_monthly_report_filters_by_status(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:monthly_documents"),
            {
                "month": "7",
                "year": "2026",
                "status": DocumentStatus.ACTIVE,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MEN-ADM-001")
        self.assertNotContains(response, "MEN-OYM-001")

    def test_invalid_monthly_report_filters_do_not_break_view(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:monthly_documents"),
            {
                "month": "13",
                "year": "invalid",
                "document_type": "999999",
                "status": "invalid",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reporte mensual documental")
        self.assertIn("report_summary", response.context)

    def test_monthly_report_selected_filters_are_kept_in_template(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:monthly_documents"),
            {
                "month": "7",
                "year": "2026",
                "document_type": self.document_type.pk,
                "organizational_unit": self.owner_unit.pk,
                "status": DocumentStatus.PUBLISHED,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="7" selected>', html=False)
        self.assertContains(response, 'value="2026"', html=False)
        self.assertContains(
            response,
            f'<option value="{self.document_type.pk}" selected>',
            html=False,
        )
        self.assertContains(
            response,
            f'<option value="{self.owner_unit.pk}" selected>',
            html=False,
        )
        self.assertContains(response, '<option value="published" selected>', html=False)

    def test_monthly_report_view_passes_clean_filters_to_selector(self):
        self.client.force_login(self.oym_admin)

        with patch(
            "apps.reports.views.get_monthly_document_report_queryset",
            return_value=DocumentVersion.objects.none(),
        ) as selector:
            response = self.client.get(
                reverse("app:reports:monthly_documents"),
                {
                    "month": "7",
                    "year": "2026",
                    "document_type": self.document_type.pk,
                    "organizational_unit": self.owner_unit.pk,
                    "status": DocumentStatus.PUBLISHED,
                },
            )

        self.assertEqual(response.status_code, 200)
        selector.assert_called_once_with(
            document_type=self.document_type,
            organizational_unit=self.owner_unit,
            status=DocumentStatus.PUBLISHED,
            date_field="published_at__date",
            date_from=date(2026, 7, 1),
            date_to=date(2026, 7, 31),
        )

    def test_controlled_copies_report_requires_login(self):
        response = self.client.get(reverse("app:reports:controlled_copies"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_oym_roles_can_view_controlled_copies_report(self):
        for user in (self.oym_admin, self.oym_analyst):
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:reports:controlled_copies"))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "reports/controlled_copies.html")
                self.assertContains(response, "Reporte de copias controladas")

    def test_disallowed_roles_cannot_view_controlled_copies_report(self):
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

                response = self.client.get(reverse("app:reports:controlled_copies"))

                self.assertEqual(response.status_code, 403)

    def test_controlled_copies_report_renders_rows_and_summary(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(reverse("app:reports:controlled_copies"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertContains(response, "PRO-ADM-001")
        self.assertContains(response, self.reader.email)
        self.assertContains(response, self.executing_unit.email)
        self.assertEqual(response.context["report_summary"]["total"], 2)
        self.assertIn(("Active", 1), response.context["report_summary"]["status_totals"])
        self.assertIn(
            ("Retired", 1),
            response.context["report_summary"]["status_totals"],
        )
        self.assertNotContains(response, "/media/")

    def test_controlled_copies_report_filters_by_status(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {"status": ControlledCopyStatus.ACTIVE},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertNotContains(response, "PRO-ADM-001")

    def test_controlled_copies_report_filters_by_document_type(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {"document_type": self.other_document_type.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PRO-ADM-001")
        self.assertNotContains(response, "FOR-OYM-001")

    def test_controlled_copies_report_filters_by_owner_unit(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {"organizational_unit": self.owner_unit.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertNotContains(response, "PRO-ADM-001")

    def test_controlled_copies_report_filters_by_receiver_unit_and_user(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {
                "receiver_unit": self.owner_unit.pk,
                "receiver_user": self.executing_unit.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PRO-ADM-001")
        self.assertNotContains(response, "FOR-OYM-001")

    def test_controlled_copies_report_filters_by_code_and_date_range(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {
                "code": "FOR-OYM-001",
                "date_from": "2026-07-01",
                "date_to": "2026-07-31",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001")
        self.assertNotContains(response, "PRO-ADM-001")

    def test_invalid_controlled_copies_filters_do_not_break_view(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {
                "document_type": "999999",
                "receiver_user": "invalid",
                "status": "invalid",
                "date_from": "not-a-date",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reporte de copias controladas")
        self.assertContains(response, "FOR-OYM-001")
        self.assertContains(response, "PRO-ADM-001")

    def test_controlled_copies_selected_filters_are_kept_in_template(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:reports:controlled_copies"),
            {
                "document_type": self.document_type.pk,
                "organizational_unit": self.owner_unit.pk,
                "receiver_unit": self.other_owner_unit.pk,
                "receiver_user": self.reader.pk,
                "status": ControlledCopyStatus.ACTIVE,
                "code": "FOR-OYM-001",
                "date_from": "2026-07-01",
                "date_to": "2026-07-31",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'<option value="{self.document_type.pk}" selected>',
            html=False,
        )
        self.assertContains(
            response,
            f'<option value="{self.owner_unit.pk}" selected>',
            html=False,
        )
        self.assertContains(
            response,
            f'<option value="{self.other_owner_unit.pk}" selected>',
            html=False,
        )
        self.assertContains(
            response,
            f'<option value="{self.reader.pk}" selected>',
            html=False,
        )
        self.assertContains(response, '<option value="active" selected>', html=False)
        self.assertContains(response, 'value="FOR-OYM-001"', html=False)
        self.assertContains(response, 'value="2026-07-01"', html=False)
        self.assertContains(response, 'value="2026-07-31"', html=False)

    def test_controlled_copies_report_passes_clean_filters_to_selector(self):
        self.client.force_login(self.oym_admin)

        with patch(
            "apps.reports.views.get_controlled_copies_report_queryset",
            return_value=ControlledCopy.objects.none(),
        ) as selector:
            response = self.client.get(
                reverse("app:reports:controlled_copies"),
                {
                    "document_type": self.document_type.pk,
                    "organizational_unit": self.owner_unit.pk,
                    "receiver_unit": self.other_owner_unit.pk,
                    "receiver_user": self.reader.pk,
                    "status": ControlledCopyStatus.ACTIVE,
                    "code": "FOR-OYM-001",
                    "date_from": "2026-07-01",
                    "date_to": "2026-07-31",
                },
            )

        self.assertEqual(response.status_code, 200)
        selector.assert_called_once_with(
            document_type=self.document_type,
            organizational_unit=self.owner_unit,
            receiver_unit=self.other_owner_unit,
            receiver_user=self.reader,
            status=ControlledCopyStatus.ACTIVE,
            code="FOR-OYM-001",
            date_from=date(2026, 7, 1),
            date_to=date(2026, 7, 31),
            date_field="delivered_at__date",
        )
