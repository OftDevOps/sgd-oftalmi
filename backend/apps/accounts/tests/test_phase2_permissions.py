from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole


class Phase2ViewPermissionTests(TestCase):
    protected_route_names = (
        "app:dashboard",
        "app:accounts:index",
        "app:organizational_units:index",
        "app:document_types:index",
        "app:documents:index",
        "app:document_requests:index",
        "app:document_requests:create",
        "app:controlled_copies:index",
        "app:implementation_records:index",
        "app:implementation_records:create",
        "app:audit:index",
        "app:reports:index",
        "app:notifications:index",
    )

    role_route_expectations = {
        UserRole.OYM_ADMIN: {
            "app:dashboard": 200,
            "app:accounts:index": 200,
            "app:organizational_units:index": 200,
            "app:document_types:index": 200,
            "app:documents:index": 200,
            "app:document_requests:index": 200,
            "app:document_requests:create": 200,
            "app:controlled_copies:index": 200,
            "app:implementation_records:index": 200,
            "app:implementation_records:create": 200,
            "app:audit:index": 200,
            "app:reports:index": 200,
            "app:notifications:index": 200,
        },
        UserRole.OYM_ANALYST: {
            "app:dashboard": 200,
            "app:accounts:index": 403,
            "app:organizational_units:index": 200,
            "app:document_types:index": 200,
            "app:documents:index": 200,
            "app:document_requests:index": 200,
            "app:document_requests:create": 200,
            "app:controlled_copies:index": 200,
            "app:implementation_records:index": 200,
            "app:implementation_records:create": 200,
            "app:audit:index": 200,
            "app:reports:index": 200,
            "app:notifications:index": 200,
        },
        UserRole.EXECUTING_UNIT: {
            "app:dashboard": 200,
            "app:accounts:index": 403,
            "app:organizational_units:index": 403,
            "app:document_types:index": 200,
            "app:documents:index": 200,
            "app:document_requests:index": 200,
            "app:document_requests:create": 200,
            "app:controlled_copies:index": 200,
            "app:implementation_records:index": 200,
            "app:implementation_records:create": 200,
            "app:audit:index": 403,
            "app:reports:index": 403,
            "app:notifications:index": 200,
        },
        UserRole.READER: {
            "app:dashboard": 200,
            "app:accounts:index": 403,
            "app:organizational_units:index": 403,
            "app:document_types:index": 403,
            "app:documents:index": 200,
            "app:document_requests:index": 403,
            "app:document_requests:create": 403,
            "app:controlled_copies:index": 200,
            "app:implementation_records:index": 200,
            "app:implementation_records:create": 200,
            "app:audit:index": 403,
            "app:reports:index": 403,
            "app:notifications:index": 200,
        },
        UserRole.SYSTEMS_TECH_ADMIN: {
            "app:dashboard": 200,
            "app:accounts:index": 200,
            "app:organizational_units:index": 200,
            "app:document_types:index": 403,
            "app:documents:index": 403,
            "app:document_requests:index": 200,
            "app:document_requests:create": 200,
            "app:controlled_copies:index": 403,
            "app:implementation_records:index": 200,
            "app:implementation_records:create": 200,
            "app:audit:index": 200,
            "app:reports:index": 403,
            "app:notifications:index": 200,
        },
        UserRole.AUDITOR: {
            "app:dashboard": 200,
            "app:accounts:index": 403,
            "app:organizational_units:index": 403,
            "app:document_types:index": 403,
            "app:documents:index": 403,
            "app:document_requests:index": 403,
            "app:document_requests:create": 403,
            "app:controlled_copies:index": 403,
            "app:implementation_records:index": 200,
            "app:implementation_records:create": 200,
            "app:audit:index": 200,
            "app:reports:index": 403,
            "app:notifications:index": 200,
        },
    }

    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"phase2-{role}@oftalmi.test",
            role=role,
        )

    def test_phase2_routes_require_login(self):
        for route_name in self.protected_route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response["Location"])

    def test_phase2_routes_apply_role_permissions(self):
        for role, route_expectations in self.role_route_expectations.items():
            with self.subTest(role=role):
                self.client.logout()
                self.client.force_login(self.create_user(role))

                for route_name, expected_status_code in route_expectations.items():
                    with self.subTest(role=role, route_name=route_name):
                        response = self.client.get(reverse(route_name))

                        self.assertEqual(response.status_code, expected_status_code)

    def test_module_access_mixin_provides_navigation_context(self):
        user = self.create_user(UserRole.OYM_ADMIN)
        self.client.force_login(user)

        for route_name in ("app:accounts:index", "app:documents:index"):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 200)
                self.assertIn("module_navigation", response.context)
                self.assertTrue(response.context["module_navigation"])
