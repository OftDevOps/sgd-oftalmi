from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.organizational_units.models import OrganizationalUnit


class OrganizationalUnitViewsTests(TestCase):
    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"{role}@oftalmi.test",
            role=role,
        )

    def setUp(self):
        self.unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
            description="Dueno funcional del MVP.",
        )
        self.inactive_unit = OrganizationalUnit.objects.create(
            name="Unidad inactiva",
            code="INAC",
            is_active=False,
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:organizational_units:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_allowed_roles_can_view_list(self):
        allowed_roles = (
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.SYSTEMS_TECH_ADMIN,
        )

        for role in allowed_roles:
            with self.subTest(role=role):
                self.client.logout()
                self.client.force_login(self.create_user(role))

                response = self.client.get(reverse("app:organizational_units:index"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Unidades ejecutoras")
                self.assertContains(response, "Organizacion y Metodos")
                self.assertContains(response, "Unidad inactiva")

    def test_disallowed_role_cannot_view_list(self):
        self.client.force_login(self.create_user(UserRole.READER))

        response = self.client.get(reverse("app:organizational_units:index"))

        self.assertEqual(response.status_code, 403)

    def test_allowed_role_can_view_detail(self):
        self.client.force_login(self.create_user(UserRole.OYM_ADMIN))

        response = self.client.get(
            reverse("app:organizational_units:detail", args=[self.unit.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Organizacion y Metodos")
        self.assertContains(response, "Dueno funcional del MVP.")

    def test_disallowed_role_cannot_view_detail(self):
        self.client.force_login(self.create_user(UserRole.EXECUTING_UNIT))

        response = self.client.get(
            reverse("app:organizational_units:detail", args=[self.unit.pk])
        )

        self.assertEqual(response.status_code, 403)
