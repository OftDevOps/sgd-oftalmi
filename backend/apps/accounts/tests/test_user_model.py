from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from apps.accounts.models import ROLE_GROUP_NAMES, UserRole
from apps.organizational_units.models import OrganizationalUnit


class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = get_user_model().objects.create_user(
            email="person@OFTALMI.COM",
            password="test-pass",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.email, "person@oftalmi.com")
        self.assertEqual(user.USERNAME_FIELD, "email")
        self.assertTrue(user.check_password("test-pass"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, UserRole.READER)
        self.assertTrue(user.is_reader)
        self.assertFalse(user.is_technical_user)

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="test-pass")

    def test_create_superuser_sets_required_flags(self):
        user = get_user_model().objects.create_superuser(
            email="admin@oftalmi.com",
            password="test-pass",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_rejects_invalid_flags(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email="admin@oftalmi.com",
                password="test-pass",
                is_staff=False,
            )

    def test_user_can_be_assigned_role_and_organizational_unit(self):
        unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        user = get_user_model().objects.create_user(
            email="analyst@oftalmi.com",
            password="test-pass",
            role=UserRole.OYM_ANALYST,
            organizational_unit=unit,
        )

        self.assertEqual(user.role, UserRole.OYM_ANALYST)
        self.assertEqual(user.organizational_unit, unit)
        self.assertTrue(user.is_oym_analyst)
        self.assertEqual(user.get_role_group_name(), "OYM_ANALYST")

    def test_systems_technical_user_role_flags(self):
        user = get_user_model().objects.create_user(
            email="systems@oftalmi.com",
            password="test-pass",
            role=UserRole.SYSTEMS_TECH_ADMIN,
            is_technical_user=True,
        )

        self.assertTrue(user.is_systems_tech_admin)
        self.assertTrue(user.is_technical_user)
        self.assertEqual(user.get_role_group_name(), "SYSTEMS_TECH_ADMIN")

    def test_role_group_names_are_defined_for_all_roles(self):
        self.assertEqual(set(ROLE_GROUP_NAMES.keys()), set(UserRole.values))
        self.assertEqual(
            set(ROLE_GROUP_NAMES.values()),
            {
                "OYM_ADMIN",
                "OYM_ANALYST",
                "EXECUTING_UNIT",
                "READER",
                "SYSTEMS_TECH_ADMIN",
                "AUDITOR",
            },
        )

    def test_base_role_groups_exist_after_migrations(self):
        expected_group_names = set(ROLE_GROUP_NAMES.values())

        existing_group_names = set(
            Group.objects.filter(name__in=expected_group_names).values_list(
                "name",
                flat=True,
            )
        )

        self.assertEqual(existing_group_names, expected_group_names)

    def test_role_helper_methods(self):
        role_expectations = {
            UserRole.OYM_ADMIN: "is_oym_admin",
            UserRole.OYM_ANALYST: "is_oym_analyst",
            UserRole.EXECUTING_UNIT: "is_executing_unit_user",
            UserRole.READER: "is_reader",
            UserRole.SYSTEMS_TECH_ADMIN: "is_systems_tech_admin",
            UserRole.AUDITOR: "is_auditor",
        }

        for role, helper_name in role_expectations.items():
            with self.subTest(role=role):
                user = get_user_model().objects.create_user(
                    email=f"{role}@oftalmi.com",
                    password="test-pass",
                    role=role,
                )

                self.assertTrue(getattr(user, helper_name))
                self.assertTrue(user.has_role(role))
