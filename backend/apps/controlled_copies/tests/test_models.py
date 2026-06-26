from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.controlled_copies.models import ControlledCopy, ControlledCopyStatus
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentVersion
from apps.organizational_units.models import OrganizationalUnit


class ControlledCopyModelTests(TestCase):
    def setUp(self):
        self.oym_user = get_user_model().objects.create_user(
            email="oym@example.com",
            password="test-pass",
        )
        self.receiver_user = get_user_model().objects.create_user(
            email="receptor@example.com",
            password="test-pass",
        )
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.receiver_unit = OrganizationalUnit.objects.create(
            name="Produccion",
            code="PROD",
        )
        self.document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro de Copias Controladas",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_user,
        )
        self.document_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="01",
            created_by=self.oym_user,
        )

    def create_controlled_copy(self, **kwargs):
        defaults = {
            "document": self.document,
            "document_version": self.document_version,
            "copy_number": "CC-001",
            "receiver_unit": self.receiver_unit,
            "created_by": self.oym_user,
        }
        defaults.update(kwargs)
        return ControlledCopy.objects.create(**defaults)

    def test_create_minimal_controlled_copy(self):
        controlled_copy = self.create_controlled_copy()

        self.assertEqual(controlled_copy.document, self.document)
        self.assertEqual(controlled_copy.document_version, self.document_version)
        self.assertEqual(controlled_copy.copy_number, "CC-001")
        self.assertEqual(controlled_copy.receiver_unit, self.receiver_unit)
        self.assertEqual(controlled_copy.created_by, self.oym_user)

    def test_controlled_copy_defaults_to_registered_status(self):
        controlled_copy = self.create_controlled_copy()

        self.assertEqual(controlled_copy.status, ControlledCopyStatus.REGISTERED)

    def test_controlled_copy_string_representation(self):
        controlled_copy = self.create_controlled_copy()

        self.assertEqual(str(controlled_copy), "FOR-OYM-001 - copy CC-001")

    def test_create_controlled_copy_with_receiver_user(self):
        controlled_copy = self.create_controlled_copy(receiver_user=self.receiver_user)

        self.assertEqual(controlled_copy.receiver_user, self.receiver_user)

    def test_receiver_user_is_optional(self):
        controlled_copy = self.create_controlled_copy()

        self.assertIsNone(controlled_copy.receiver_user)

    def test_create_controlled_copy_with_delivery_and_retirement_dates(self):
        delivered_at = timezone.now()
        retired_at = delivered_at + timezone.timedelta(days=30)
        controlled_copy = self.create_controlled_copy(
            status=ControlledCopyStatus.RETIRED,
            delivered_at=delivered_at,
            retired_at=retired_at,
        )

        self.assertEqual(controlled_copy.delivered_at, delivered_at)
        self.assertEqual(controlled_copy.retired_at, retired_at)
        self.assertEqual(controlled_copy.status, ControlledCopyStatus.RETIRED)

    def test_create_controlled_copy_with_observations_and_evidence_reference(self):
        controlled_copy = self.create_controlled_copy(
            observations="Entrega registrada por OyM.",
            evidence_reference="ACTA-001",
        )

        self.assertEqual(controlled_copy.observations, "Entrega registrada por OyM.")
        self.assertEqual(controlled_copy.evidence_reference, "ACTA-001")

    def test_copy_number_is_unique_per_document_version(self):
        self.create_controlled_copy()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_controlled_copy()

    def test_same_copy_number_can_be_used_for_different_document_version(self):
        other_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="02",
            created_by=self.oym_user,
        )

        self.create_controlled_copy()
        controlled_copy = self.create_controlled_copy(document_version=other_version)

        self.assertEqual(controlled_copy.copy_number, "CC-001")
        self.assertEqual(controlled_copy.document_version, other_version)

    def test_document_version_must_belong_to_selected_document(self):
        other_document = Document.objects.create(
            code="FOR-OYM-002",
            title="Documento distinto",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_user,
        )
        controlled_copy = ControlledCopy(
            document=other_document,
            document_version=self.document_version,
            copy_number="CC-002",
            receiver_unit=self.receiver_unit,
            created_by=self.oym_user,
        )

        with self.assertRaises(ValidationError):
            controlled_copy.full_clean()

    def test_can_create_controlled_copy_for_each_defined_status(self):
        for index, status in enumerate(ControlledCopyStatus.values, start=1):
            with self.subTest(status=status):
                controlled_copy = self.create_controlled_copy(
                    copy_number=f"CC-{index:03d}",
                    status=status,
                )

                self.assertEqual(controlled_copy.status, status)
