from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.audit.models import AuditAction, AuditEvent, AuditResult
from apps.audit.selectors import audit_event_list
from apps.audit.services import (
    AuditContext,
    audit_event_create,
    audit_event_create_for_instance,
    audit_event_create_if_requested,
)


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

    def test_controlled_audit_returns_none_without_context(self):
        user = get_user_model().objects.create_user(
            email="system@oftalmi.com",
            password="test-pass",
        )

        event = audit_event_create_if_requested(
            action=AuditAction.OTHER,
            module="accounts",
            instance=user,
            description="No context provided.",
        )

        self.assertIsNone(event)
        self.assertEqual(AuditEvent.objects.count(), 0)

    def test_create_audit_event_for_instance_with_context(self):
        user = get_user_model().objects.create_user(
            email="oym@oftalmi.com",
            password="test-pass",
        )
        context = AuditContext(
            user=user,
            ip_address="127.0.0.1",
            user_agent="test-agent",
        )

        event = audit_event_create_for_instance(
            audit_context=context,
            action=AuditAction.OTHER,
            module="accounts",
            instance=user,
            description="User audited.",
        )

        self.assertEqual(event.user, user)
        self.assertEqual(event.entity_type, "User")
        self.assertEqual(event.entity_id, str(user.id))
        self.assertEqual(event.ip_address, "127.0.0.1")
        self.assertEqual(event.user_agent, "test-agent")
