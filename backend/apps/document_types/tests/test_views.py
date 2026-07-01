from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.document_types.models import DocumentType


class DocumentTypeViewsTests(TestCase):
    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"{role}@oftalmi.test",
            role=role,
        )

    def setUp(self):
        self.document_type = DocumentType.objects.create(
            code="FOR",
            name="Formato",
            description="Tipo documental base.",
        )
        self.inactive_document_type = DocumentType.objects.create(
            code="DOC",
            name="Documento",
            is_active=False,
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:document_types:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_allowed_roles_can_view_list(self):
        allowed_roles = (
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
        )

        for role in allowed_roles:
            with self.subTest(role=role):
                self.client.logout()
                self.client.force_login(self.create_user(role))

                response = self.client.get(reverse("app:document_types:index"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Tipos documentales")
                self.assertContains(response, "FOR")
                self.assertContains(response, "DOC")

    def test_disallowed_role_cannot_view_list(self):
        self.client.force_login(self.create_user(UserRole.READER))

        response = self.client.get(reverse("app:document_types:index"))

        self.assertEqual(response.status_code, 403)

    def test_allowed_role_can_view_detail(self):
        self.client.force_login(self.create_user(UserRole.OYM_ADMIN))

        response = self.client.get(
            reverse("app:document_types:detail", args=[self.document_type.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR - Formato")
        self.assertContains(response, "Tipo documental base.")

    def test_disallowed_role_cannot_view_detail(self):
        self.client.force_login(self.create_user(UserRole.SYSTEMS_TECH_ADMIN))

        response = self.client.get(
            reverse("app:document_types:detail", args=[self.document_type.pk])
        )

        self.assertEqual(response.status_code, 403)
