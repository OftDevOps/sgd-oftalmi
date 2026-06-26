from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import UserRole
from apps.document_requests.permissions import (
    can_create_document_request,
    can_process_document_request,
    can_view_all_document_requests,
)


class DocumentRequestPermissionTests(TestCase):
    def create_user(self, role):
        return get_user_model().objects.create_user(
            email=f"{role}@oftalmi.com",
            password="test-pass",
            role=role,
        )

    def test_executing_unit_can_create_but_not_process_requests(self):
        user = self.create_user(UserRole.EXECUTING_UNIT)

        self.assertTrue(can_create_document_request(user))
        self.assertFalse(can_view_all_document_requests(user))
        self.assertFalse(can_process_document_request(user))

    def test_oym_roles_can_process_requests(self):
        user = self.create_user(UserRole.OYM_ANALYST)

        self.assertTrue(can_create_document_request(user))
        self.assertTrue(can_view_all_document_requests(user))
        self.assertTrue(can_process_document_request(user))
