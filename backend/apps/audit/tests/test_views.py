from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.audit.models import AuditAction, AuditEvent, AuditResult


class AuditEventViewsTests(TestCase):
    def create_user(self, role, prefix):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
        )

    def setUp(self):
        self.oym_admin = self.create_user(UserRole.OYM_ADMIN, "oym-admin")
        self.oym_analyst = self.create_user(UserRole.OYM_ANALYST, "oym-analyst")
        self.auditor = self.create_user(UserRole.AUDITOR, "auditor")
        self.systems_user = self.create_user(UserRole.SYSTEMS_TECH_ADMIN, "systems")
        self.reader = self.create_user(UserRole.READER, "reader")
        self.executing_unit = self.create_user(UserRole.EXECUTING_UNIT, "executing-unit")
        self.event = AuditEvent.objects.create(
            user=self.oym_admin,
            action=AuditAction.DOCUMENT_CREATED,
            module="documents",
            entity_type="Document",
            entity_id="10",
            result=AuditResult.SUCCESS,
            ip_address="127.0.0.1",
            user_agent="test-agent",
            description="Documento creado.",
            before_data={"status": "draft"},
            after_data={"status": "received"},
        )
        self.system_event = AuditEvent.objects.create(
            action=AuditAction.REPORT_GENERATED,
            module="reports",
            entity_type="ReportExport",
            entity_id="20",
            result=AuditResult.WARNING,
            description="Evento tecnico sin usuario.",
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:audit:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_allowed_roles_can_view_audit_list(self):
        allowed_users = (
            self.oym_admin,
            self.oym_analyst,
            self.auditor,
            self.systems_user,
        )

        for user in allowed_users:
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:audit:index"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Auditoria")
                self.assertContains(response, "documents")
                self.assertContains(response, "reports")

    def test_disallowed_roles_cannot_view_audit_list(self):
        denied_users = (
            self.reader,
            self.executing_unit,
        )

        for user in denied_users:
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:audit:index"))

                self.assertEqual(response.status_code, 403)

    def test_allowed_role_can_view_audit_detail(self):
        self.client.force_login(self.auditor)

        response = self.client.get(reverse("app:audit:detail", args=[self.event.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "documents - Document created")
        self.assertContains(response, "Documento creado.")
        self.assertContains(response, "127.0.0.1")
        self.assertContains(response, "test-agent")
        self.assertContains(response, "draft")
        self.assertContains(response, "received")

    def test_disallowed_role_cannot_view_audit_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(reverse("app:audit:detail", args=[self.event.pk]))

        self.assertEqual(response.status_code, 403)

    def test_no_export_or_create_routes_are_exposed(self):
        self.client.force_login(self.oym_admin)

        self.assertEqual(self.client.get("/app/audit/export/").status_code, 404)
        self.assertEqual(self.client.get("/app/audit/new/").status_code, 404)
