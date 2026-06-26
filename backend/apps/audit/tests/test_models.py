from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.audit.models import AuditAction, AuditEvent, AuditResult


class AuditEventModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="auditor@example.com",
            password="test-pass",
        )

    def create_audit_event(self, **kwargs):
        defaults = {
            "user": self.user,
            "action": AuditAction.DOCUMENT_CREATED,
            "module": "documents",
            "entity_type": "Document",
            "entity_id": "1",
            "result": AuditResult.SUCCESS,
            "description": "Document created from OyM process.",
        }
        defaults.update(kwargs)
        return AuditEvent.objects.create(**defaults)

    def test_create_minimal_audit_event(self):
        event = self.create_audit_event()

        self.assertEqual(event.user, self.user)
        self.assertEqual(event.action, AuditAction.DOCUMENT_CREATED)
        self.assertEqual(event.module, "documents")
        self.assertEqual(event.entity_type, "Document")
        self.assertEqual(event.entity_id, "1")
        self.assertEqual(event.result, AuditResult.SUCCESS)
        self.assertIsNotNone(event.created_at)

    def test_audit_event_can_be_system_event_without_user(self):
        event = self.create_audit_event(
            user=None,
            action=AuditAction.REPORT_GENERATED,
            module="reports",
            entity_type="",
            entity_id="",
        )

        self.assertIsNone(event.user)
        self.assertEqual(event.module, "reports")

    def test_audit_event_string_representation(self):
        event = self.create_audit_event()

        self.assertEqual(event.__str__(), "documents - Document created - Success")

    def test_audit_event_can_store_ip_and_user_agent(self):
        event = self.create_audit_event(
            ip_address="192.168.1.10",
            user_agent="Mozilla/5.0",
        )

        self.assertEqual(event.ip_address, "192.168.1.10")
        self.assertEqual(event.user_agent, "Mozilla/5.0")

    def test_audit_event_can_store_before_and_after_data(self):
        event = self.create_audit_event(
            before_data={"status": "draft"},
            after_data={"status": "active"},
        )

        self.assertEqual(event.before_data, {"status": "draft"})
        self.assertEqual(event.after_data, {"status": "active"})

    def test_audit_event_keeps_user_relation_nullable_after_user_delete(self):
        event = self.create_audit_event()

        self.user.delete()
        event.refresh_from_db()

        self.assertIsNone(event.user)

    def test_can_create_audit_event_for_each_defined_result(self):
        for index, result in enumerate(AuditResult.values, start=1):
            with self.subTest(result=result):
                event = self.create_audit_event(
                    action=AuditAction.OTHER,
                    module=f"module_{index}",
                    result=result,
                )

                self.assertEqual(event.result, result)

    def test_can_create_audit_event_for_each_defined_action(self):
        for index, action in enumerate(AuditAction.values, start=1):
            with self.subTest(action=action):
                event = self.create_audit_event(
                    action=action,
                    module=f"module_action_{index}",
                )

                self.assertEqual(event.action, action)
