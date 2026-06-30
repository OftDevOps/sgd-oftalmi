from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole


class AccessURLTests(TestCase):
    module_url_names = (
        "app:accounts:index",
        "app:organizational_units:index",
        "app:document_types:index",
        "app:documents:index",
        "app:document_requests:index",
        "app:controlled_copies:index",
        "app:implementation_records:index",
        "app:audit:index",
        "app:reports:index",
        "app:notifications:index",
    )

    def create_user(self, role=UserRole.OYM_ADMIN, email="user@oftalmi.test"):
        return get_user_model().objects.create_user(email=email, role=role)

    def test_root_redirects_to_app_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("app:dashboard"))

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Correo institucional")

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("app:dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_module_urls_require_authentication(self):
        for url_name in self.module_url_names:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response["Location"])

    def test_oym_admin_can_access_base_module_urls(self):
        user = self.create_user()
        self.client.force_login(user)

        for url_name in self.module_url_names:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Base de acceso")

    def test_reader_access_is_limited_by_module_permissions(self):
        user = self.create_user(
            role=UserRole.READER,
            email="reader@oftalmi.test",
        )
        self.client.force_login(user)

        self.assertEqual(self.client.get(reverse("app:documents:index")).status_code, 200)
        self.assertEqual(
            self.client.get(reverse("app:notifications:index")).status_code,
            200,
        )
        self.assertEqual(self.client.get(reverse("app:reports:index")).status_code, 403)
        self.assertEqual(self.client.get(reverse("app:audit:index")).status_code, 403)

    def test_api_v1_index_requires_authentication(self):
        response = self.client.get(reverse("api_v1_index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_api_v1_index_returns_reserved_metadata_for_authenticated_user(self):
        user = self.create_user()
        self.client.force_login(user)

        response = self.client.get(reverse("api_v1_index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "reserved")
        self.assertFalse(response.json()["public"])
