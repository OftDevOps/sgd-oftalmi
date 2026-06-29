from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.audit.models import AuditAction, AuditEvent
from apps.audit.services import AuditContext
from apps.document_requests.models import DocumentRequestStatus, DocumentRequestType
from apps.document_requests.services import (
    document_request_create,
    document_request_transition_status,
)
from apps.document_requests.workflows import (
    can_transition_document_request_status,
    get_allowed_document_request_status_transitions,
)
from apps.organizational_units.models import OrganizationalUnit


class DocumentRequestWorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="solicitante@oftalmi.com",
            password="test-pass",
        )
        self.unit = OrganizationalUnit.objects.create(name="Produccion", code="PROD")

    def create_request(self, **kwargs):
        defaults = {
            "request_type": DocumentRequestType.CREATE,
            "title": "Solicitud documental",
            "requested_by": self.user,
            "organizational_unit": self.unit,
        }
        defaults.update(kwargs)
        return document_request_create(**defaults)

    def test_allowed_document_request_status_transitions_are_explicit(self):
        self.assertIn(
            DocumentRequestStatus.SUBMITTED,
            get_allowed_document_request_status_transitions(DocumentRequestStatus.DRAFT),
        )
        self.assertTrue(
            can_transition_document_request_status(
                DocumentRequestStatus.SUBMITTED,
                DocumentRequestStatus.RECEIVED,
            )
        )
        self.assertFalse(
            can_transition_document_request_status(
                DocumentRequestStatus.DRAFT,
                DocumentRequestStatus.CLOSED,
            )
        )

    def test_transition_from_draft_to_submitted_sets_submitted_at(self):
        document_request = self.create_request()
        changed_at = timezone.now()

        document_request_transition_status(
            document_request=document_request,
            target_status=DocumentRequestStatus.SUBMITTED,
            changed_at=changed_at,
        )

        document_request.refresh_from_db()
        self.assertEqual(document_request.status, DocumentRequestStatus.SUBMITTED)
        self.assertEqual(document_request.submitted_at, changed_at)

    def test_transition_from_submitted_to_received(self):
        document_request = self.create_request(status=DocumentRequestStatus.SUBMITTED)

        document_request_transition_status(
            document_request=document_request,
            target_status=DocumentRequestStatus.RECEIVED,
        )

        document_request.refresh_from_db()
        self.assertEqual(document_request.status, DocumentRequestStatus.RECEIVED)

    def test_observed_request_can_be_resubmitted(self):
        document_request = self.create_request(status=DocumentRequestStatus.OBSERVED)

        document_request_transition_status(
            document_request=document_request,
            target_status=DocumentRequestStatus.SUBMITTED,
        )

        document_request.refresh_from_db()
        self.assertEqual(document_request.status, DocumentRequestStatus.SUBMITTED)
        self.assertIsNotNone(document_request.submitted_at)

    def test_transition_to_closed_sets_closed_at(self):
        document_request = self.create_request(status=DocumentRequestStatus.IN_REVIEW)
        changed_at = timezone.now()

        document_request_transition_status(
            document_request=document_request,
            target_status=DocumentRequestStatus.CLOSED,
            changed_at=changed_at,
        )

        document_request.refresh_from_db()
        self.assertEqual(document_request.status, DocumentRequestStatus.CLOSED)
        self.assertEqual(document_request.closed_at, changed_at)

    def test_transition_creates_audit_event_when_context_is_provided(self):
        document_request = self.create_request(status=DocumentRequestStatus.SUBMITTED)

        document_request_transition_status(
            document_request=document_request,
            target_status=DocumentRequestStatus.RECEIVED,
            audit_context=AuditContext(user=self.user),
        )

        event = AuditEvent.objects.get()
        self.assertEqual(event.action, AuditAction.OTHER)
        self.assertEqual(event.module, "document_requests")
        self.assertEqual(event.entity_type, "DocumentRequest")
        self.assertEqual(event.entity_id, str(document_request.id))
        self.assertEqual(event.before_data, {"status": DocumentRequestStatus.SUBMITTED})
        self.assertEqual(event.after_data, {"status": DocumentRequestStatus.RECEIVED})

    def test_invalid_transition_raises_validation_error(self):
        document_request = self.create_request(status=DocumentRequestStatus.DRAFT)

        with self.assertRaises(ValidationError):
            document_request_transition_status(
                document_request=document_request,
                target_status=DocumentRequestStatus.CLOSED,
            )

    def test_cancelled_request_is_terminal(self):
        document_request = self.create_request(status=DocumentRequestStatus.CANCELLED)

        with self.assertRaises(ValidationError):
            document_request_transition_status(
                document_request=document_request,
                target_status=DocumentRequestStatus.SUBMITTED,
            )
