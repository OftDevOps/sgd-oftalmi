from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.audit.models import AuditAction, AuditResult
from apps.audit.selectors import audit_event_list
from apps.audit.services import audit_event_create


class AuditServicesSelectorsTests(TestCase):
    def test_create_audit_event_and_filter_by_module(self):
        user = get_user_model().objects.create_user(
            email="auditor@oftalmi.com",
            password="test-pass",
        )

        event = audit_event_create(
            user=user,
            action=AuditAction.DOCUMENT_CREATED,
            module="documents",
            result=AuditResult.SUCCESS,
            entity_type="Document",
            entity_id="1",
        )

        self.assertEqual(list(audit_event_list(module="documents")), [event])
