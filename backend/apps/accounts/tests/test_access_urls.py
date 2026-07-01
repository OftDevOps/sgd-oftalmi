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

    def create_user(
        self,
        role=UserRole.OYM_ADMIN,
        email="user@oftalmi.test",
        password="secure-pass",
    ):
        return get_user_model().objects.create_user(
            email=email,
            password=password,
            role=role,
        )

    def test_root_redirects_anonymous_user_to_login(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("login"))

    def test_root_redirects_authenticated_user_by_role(self):
        user = self.create_user(role=UserRole.READER)
        self.client.force_login(user)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("app:documents:index"))

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Correo institucional")

    def test_login_redirects_authenticated_user_by_role(self):
        user = self.create_user(role=UserRole.SYSTEMS_TECH_ADMIN)
        self.client.force_login(user)

        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("app:accounts:index"))

    def test_login_post_redirects_user_by_role(self):
        role_redirects = (
            (UserRole.OYM_ADMIN, "app:documents:index"),
            (UserRole.OYM_ANALYST, "app:documents:index"),
            (UserRole.EXECUTING_UNIT, "app:document_requests:index"),
            (UserRole.READER, "app:documents:index"),
            (UserRole.SYSTEMS_TECH_ADMIN, "app:accounts:index"),
            (UserRole.AUDITOR, "app:audit:index"),
        )

        for role, url_name in role_redirects:
            with self.subTest(role=role):
                self.client.logout()
                user = self.create_user(
                    role=role,
                    email=f"{role}@oftalmi.test",
                    password="secure-pass",
                )

                response = self.client.post(
                    reverse("login"),
                    {
                        "username": user.email,
                        "password": "secure-pass",
                    },
                )

                self.assertEqual(response.status_code, 302)
                self.assertEqual(response["Location"], reverse(url_name))

    def test_login_post_respects_safe_next_parameter(self):
        user = self.create_user(password="secure-pass")
        next_url = reverse("app:audit:index")

        response = self.client.post(
            f"{reverse('login')}?next={next_url}",
            {
                "username": user.email,
                "password": "secure-pass",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], next_url)

    def test_logout_post_redirects_to_logged_out_page(self):
        user = self.create_user()
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("logged_out"))

        logged_out_response = self.client.get(reverse("logged_out"))
        self.assertEqual(logged_out_response.status_code, 200)
        self.assertContains(logged_out_response, "Sesion cerrada")

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("app:dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_dashboard_displays_role_specific_content(self):
        role_expectations = (
            (UserRole.OYM_ADMIN, "Operacion documental OyM", "Solicitudes documentales"),
            (UserRole.OYM_ANALYST, "Gestion operativa OyM", "Copias controladas"),
            (UserRole.EXECUTING_UNIT, "Unidad ejecutora", "Solicitudes documentales"),
            (UserRole.READER, "Consulta e implementacion", "Notificaciones"),
            (UserRole.SYSTEMS_TECH_ADMIN, "Operacion tecnica", "Usuarios"),
            (UserRole.AUDITOR, "Consulta de auditoria", "Auditoria"),
        )

        for role, title, action in role_expectations:
            with self.subTest(role=role):
                self.client.logout()
                user = self.create_user(
                    role=role,
                    email=f"dashboard-{role}@oftalmi.test",
                )
                self.client.force_login(user)

                response = self.client.get(reverse("app:dashboard"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, title)
                self.assertContains(response, action)

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
