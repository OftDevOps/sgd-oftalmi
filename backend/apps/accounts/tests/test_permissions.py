from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import UserRole
from apps.accounts.permissions import (
    can_change_user_roles,
    can_manage_users,
    can_view_users,
)


class AccountPermissionTests(TestCase):
    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"{role}@oftalmi.com",
            password="test-pass",
            role=role,
        )

    def test_oym_admin_can_manage_users_and_change_roles(self):
        user = self.create_user(UserRole.OYM_ADMIN)

        self.assertTrue(can_view_users(user))
        self.assertTrue(can_manage_users(user))
        self.assertTrue(can_change_user_roles(user))

    def test_systems_can_manage_users_but_not_change_functional_roles(self):
        user = self.create_user(UserRole.SYSTEMS_TECH_ADMIN)

        self.assertTrue(can_view_users(user))
        self.assertTrue(can_manage_users(user))
        self.assertFalse(can_change_user_roles(user))

    def test_reader_cannot_manage_users(self):
        user = self.create_user(UserRole.READER)

        self.assertFalse(can_view_users(user))
        self.assertFalse(can_manage_users(user))
