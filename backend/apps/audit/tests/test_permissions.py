from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import UserRole
from apps.audit.permissions import (
    can_export_audit,
    can_modify_audit,
    can_view_audit,
    can_view_functional_audit,
    can_view_technical_audit,
)


class AuditPermissionTests(TestCase):
    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"{role}@oftalmi.com",
            password="test-pass",
            role=role,
        )

    def test_auditor_can_view_and_export_but_not_modify_audit(self):
        user = self.create_user(UserRole.AUDITOR)

        self.assertTrue(can_view_audit(user))
        self.assertTrue(can_export_audit(user))
        self.assertFalse(can_modify_audit(user))

    def test_oym_roles_can_view_functional_audit(self):
        for role in (UserRole.OYM_ADMIN, UserRole.OYM_ANALYST):
            with self.subTest(role=role):
                user = self.create_user(role)

                self.assertTrue(can_view_functional_audit(user))
                self.assertTrue(can_view_audit(user))

    def test_systems_can_view_technical_audit_only(self):
        user = self.create_user(UserRole.SYSTEMS_TECH_ADMIN)

        self.assertTrue(can_view_technical_audit(user))
        self.assertTrue(can_view_audit(user))
        self.assertFalse(can_export_audit(user))

    def test_reader_and_executing_unit_cannot_view_audit(self):
        for role in (UserRole.READER, UserRole.EXECUTING_UNIT):
            with self.subTest(role=role):
                user = self.create_user(role)

                self.assertFalse(can_view_audit(user))
