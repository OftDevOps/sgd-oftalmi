from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.audit.models import AuditAction, AuditEvent
from apps.audit.services import AuditContext
from apps.controlled_copies.models import ControlledCopyStatus
from apps.controlled_copies.selectors import active_controlled_copy_list, controlled_copy_list
from apps.controlled_copies.services import (
    controlled_copy_create,
    controlled_copy_register_delivery,
    controlled_copy_register_retirement,
)
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentVersion
from apps.organizational_units.models import OrganizationalUnit


class ControlledCopyServicesSelectorsTests(TestCase):
    def test_create_controlled_copy_and_filter_active(self):
        user = get_user_model().objects.create_user(email="oym@oftalmi.com", password="test-pass")
        document_type = DocumentType.objects.create(code="FOR", name="Formato")
        owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        receiver_unit = OrganizationalUnit.objects.create(name="Produccion", code="PROD")
        document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro",
            document_type=document_type,
            owner_unit=owner_unit,
            created_by=user,
        )
        version = DocumentVersion.objects.create(document=document, version_number="01", created_by=user)

        copy = controlled_copy_create(
            document=document,
            document_version=version,
            copy_number="CC-001",
            receiver_unit=receiver_unit,
            created_by=user,
            status=ControlledCopyStatus.ACTIVE,
        )

        self.assertEqual(list(active_controlled_copy_list()), [copy])
        self.assertEqual(list(controlled_copy_list(receiver_unit=receiver_unit)), [copy])

    def test_delivery_and_retirement_services_create_audit_events_with_context(self):
        user = get_user_model().objects.create_user(email="oym@oftalmi.com", password="test-pass")
        document_type = DocumentType.objects.create(code="FOR", name="Formato")
        owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        receiver_unit = OrganizationalUnit.objects.create(name="Produccion", code="PROD")
        document = Document.objects.create(
            code="FOR-OYM-002",
            title="Registro",
            document_type=document_type,
            owner_unit=owner_unit,
            created_by=user,
        )
        version = DocumentVersion.objects.create(document=document, version_number="01", created_by=user)
        controlled_copy = controlled_copy_create(
            document=document,
            document_version=version,
            copy_number="CC-002",
            receiver_unit=receiver_unit,
            created_by=user,
        )
        context = AuditContext(user=user)

        controlled_copy_register_delivery(
            controlled_copy=controlled_copy,
            audit_context=context,
        )
        controlled_copy_register_retirement(
            controlled_copy=controlled_copy,
            audit_context=context,
        )

        self.assertEqual(
            list(AuditEvent.objects.values_list("action", flat=True)),
            [
                AuditAction.CONTROLLED_COPY_RETIRED,
                AuditAction.CONTROLLED_COPY_DELIVERED,
            ],
        )
