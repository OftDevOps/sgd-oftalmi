from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.audit.models import AuditAction, AuditEvent
from apps.audit.services import AuditContext
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentVersion
from apps.implementation_records.models import ImplementationRecordStatus
from apps.implementation_records.selectors import pending_implementation_record_list
from apps.implementation_records.services import implementation_record_create
from apps.organizational_units.models import OrganizationalUnit


class ImplementationRecordServicesSelectorsTests(TestCase):
    def test_create_implementation_record_and_filter_pending(self):
        user = get_user_model().objects.create_user(email="lector@oftalmi.com", password="test-pass")
        oym_user = get_user_model().objects.create_user(email="oym@oftalmi.com", password="test-pass")
        document_type = DocumentType.objects.create(code="FOR", name="Formato")
        owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro",
            document_type=document_type,
            owner_unit=owner_unit,
            created_by=oym_user,
        )
        version = DocumentVersion.objects.create(document=document, version_number="01", created_by=oym_user)

        record = implementation_record_create(
            user=user,
            document=document,
            document_version=version,
            status=ImplementationRecordStatus.PENDING,
        )

        self.assertEqual(list(pending_implementation_record_list(user=user)), [record])

    def test_create_implementation_record_creates_audit_event_when_context_is_provided(self):
        user = get_user_model().objects.create_user(email="lector2@oftalmi.com", password="test-pass")
        oym_user = get_user_model().objects.create_user(email="oym2@oftalmi.com", password="test-pass")
        document_type = DocumentType.objects.create(code="INS", name="Instructivo")
        owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM2")
        document = Document.objects.create(
            code="INS-OYM-001",
            title="Registro",
            document_type=document_type,
            owner_unit=owner_unit,
            created_by=oym_user,
        )
        version = DocumentVersion.objects.create(document=document, version_number="01", created_by=oym_user)

        record = implementation_record_create(
            user=user,
            document=document,
            document_version=version,
            audit_context=AuditContext(user=oym_user),
        )

        event = AuditEvent.objects.get()
        self.assertEqual(event.action, AuditAction.IMPLEMENTATION_RECORD_REGISTERED)
        self.assertEqual(event.module, "implementation_records")
        self.assertEqual(event.entity_id, str(record.id))
