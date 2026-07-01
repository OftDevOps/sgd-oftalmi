from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import UserRole
from apps.controlled_copies.permissions import can_view_controlled_copies


class ControlledCopyPermissionTests(TestCase):
    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"{role}@oftalmi.test",
            role=role,
        )

    def test_oym_and_recipient_roles_can_access_controlled_copy_consultation(self):
        allowed_roles = (
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        )

        for role in allowed_roles:
            with self.subTest(role=role):
                self.assertTrue(can_view_controlled_copies(self.create_user(role)))

    def test_systems_and_auditor_do_not_access_without_defined_helper_permission(self):
        denied_roles = (
            UserRole.SYSTEMS_TECH_ADMIN,
            UserRole.AUDITOR,
        )

        for role in denied_roles:
            with self.subTest(role=role):
                self.assertFalse(can_view_controlled_copies(self.create_user(role)))
