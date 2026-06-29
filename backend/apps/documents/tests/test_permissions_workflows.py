from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import UserRole
from apps.audit.models import AuditAction, AuditEvent
from apps.audit.services import AuditContext
from apps.document_types.models import DocumentType
from apps.documents.models import DocumentStatus
from apps.documents.permissions import (
    can_copy_document,
    can_create_document,
    can_decommission_document,
    can_download_document,
    can_publish_document,
    can_view_assigned_document,
    can_view_obsolete_document,
)
from apps.documents.services import document_create, document_transition_status
from apps.documents.workflows import (
    can_transition_document_status,
    get_allowed_document_status_transitions,
)
from apps.organizational_units.models import OrganizationalUnit


class DocumentPermissionWorkflowTests(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        self.oym_admin = self.create_user(UserRole.OYM_ADMIN, "oym_admin")
        self.oym_analyst = self.create_user(UserRole.OYM_ANALYST, "oym_analyst")
        self.reader = self.create_user(UserRole.READER, "reader")

    def create_user(self, role, prefix):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.com",
            password="test-pass",
            role=role,
        )

    def test_document_permissions_by_role(self):
        self.assertTrue(can_create_document(self.oym_admin))
        self.assertTrue(can_create_document(self.oym_analyst))
        self.assertFalse(can_create_document(self.reader))
        self.assertTrue(can_publish_document(self.oym_admin))
        self.assertFalse(can_publish_document(self.oym_analyst))
        self.assertTrue(can_decommission_document(self.oym_admin))
        self.assertTrue(can_view_obsolete_document(self.oym_analyst))

    def test_reader_can_view_only_assigned_document_and_never_download_copy_or_print(self):
        self.assertTrue(can_view_assigned_document(self.reader, is_assigned=True))
        self.assertFalse(can_view_assigned_document(self.reader, is_assigned=False))
        self.assertFalse(can_download_document(self.reader))
        self.assertFalse(can_copy_document(self.reader))

    def test_allowed_document_status_transitions_are_explicit(self):
        self.assertIn(
            DocumentStatus.UNDER_REVIEW,
            get_allowed_document_status_transitions(DocumentStatus.RECEIVED),
        )
        self.assertTrue(
            can_transition_document_status(
                DocumentStatus.UNDER_REVIEW,
                DocumentStatus.APPROVED,
            )
        )
        self.assertFalse(
            can_transition_document_status(
                DocumentStatus.DRAFT,
                DocumentStatus.OBSOLETE,
            )
        )

    def test_document_transition_status_updates_valid_transition(self):
        document = document_create(
            code="FOR-OYM-001",
            title="Registro",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.RECEIVED,
        )

        document_transition_status(
            document=document,
            target_status=DocumentStatus.UNDER_REVIEW,
        )

        document.refresh_from_db()
        self.assertEqual(document.status, DocumentStatus.UNDER_REVIEW)

    def test_document_transition_status_creates_audit_event_when_context_is_provided(self):
        document = document_create(
            code="FOR-OYM-003",
            title="Registro auditado",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.RECEIVED,
        )

        document_transition_status(
            document=document,
            target_status=DocumentStatus.UNDER_REVIEW,
            audit_context=AuditContext(user=self.oym_admin),
        )

        event = AuditEvent.objects.get()
        self.assertEqual(event.action, AuditAction.DOCUMENT_STATUS_CHANGED)
        self.assertEqual(event.module, "documents")
        self.assertEqual(event.entity_type, "Document")
        self.assertEqual(event.entity_id, str(document.id))
        self.assertEqual(event.before_data, {"status": DocumentStatus.RECEIVED})
        self.assertEqual(event.after_data, {"status": DocumentStatus.UNDER_REVIEW})

    def test_document_transition_status_rejects_invalid_transition(self):
        document = document_create(
            code="FOR-OYM-002",
            title="Registro invalido",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.DRAFT,
        )

        with self.assertRaises(ValidationError):
            document_transition_status(
                document=document,
                target_status=DocumentStatus.OBSOLETE,
            )
