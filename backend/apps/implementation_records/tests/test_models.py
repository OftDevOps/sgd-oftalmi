from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentVersion
from apps.implementation_records.models import (
    ImplementationRecord,
    ImplementationRecordStatus,
)
from apps.organizational_units.models import OrganizationalUnit


class ImplementationRecordModelTests(TestCase):
    def setUp(self):
        self.oym_user = get_user_model().objects.create_user(
            email="oym@example.com",
            password="test-pass",
        )
        self.assigned_user = get_user_model().objects.create_user(
            email="lector@example.com",
            password="test-pass",
        )
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.document = Document.objects.create(
            code="FOR-OYM-001",
            title="Documento para implementacion",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_user,
        )
        self.document_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="01",
            created_by=self.oym_user,
        )

    def create_implementation_record(self, **kwargs):
        defaults = {
            "user": self.assigned_user,
            "document": self.document,
            "document_version": self.document_version,
        }
        defaults.update(kwargs)
        return ImplementationRecord.objects.create(**defaults)

    def test_create_minimal_implementation_record(self):
        record = self.create_implementation_record()

        self.assertEqual(record.user, self.assigned_user)
        self.assertEqual(record.document, self.document)
        self.assertEqual(record.document_version, self.document_version)
        self.assertIsNotNone(record.assigned_at)

    def test_implementation_record_defaults_to_pending_status(self):
        record = self.create_implementation_record()

        self.assertEqual(record.status, ImplementationRecordStatus.PENDING)

    def test_implementation_record_string_representation(self):
        record = self.create_implementation_record()

        self.assertEqual(str(record), "lector@example.com - FOR-OYM-001 v01")

    def test_can_store_read_interpreted_accepted_and_implemented_dates(self):
        now = timezone.now()
        record = self.create_implementation_record(
            status=ImplementationRecordStatus.IMPLEMENTED,
            read_at=now,
            interpreted_at=now,
            accepted_at=now,
            implemented_at=now,
        )

        self.assertEqual(record.read_at, now)
        self.assertEqual(record.interpreted_at, now)
        self.assertEqual(record.accepted_at, now)
        self.assertEqual(record.implemented_at, now)
        self.assertEqual(record.status, ImplementationRecordStatus.IMPLEMENTED)

    def test_user_document_version_must_be_unique(self):
        self.create_implementation_record()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_implementation_record()

    def test_same_user_can_have_new_record_for_new_document_version(self):
        new_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="02",
            created_by=self.oym_user,
        )

        self.create_implementation_record()
        record = self.create_implementation_record(document_version=new_version)

        self.assertEqual(record.user, self.assigned_user)
        self.assertEqual(record.document_version, new_version)

    def test_different_users_can_have_record_for_same_document_version(self):
        other_user = get_user_model().objects.create_user(
            email="lector2@example.com",
            password="test-pass",
        )

        self.create_implementation_record()
        record = self.create_implementation_record(user=other_user)

        self.assertEqual(record.user, other_user)
        self.assertEqual(record.document_version, self.document_version)

    def test_document_version_must_belong_to_selected_document(self):
        other_document = Document.objects.create(
            code="FOR-OYM-002",
            title="Documento distinto",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_user,
        )
        record = ImplementationRecord(
            user=self.assigned_user,
            document=other_document,
            document_version=self.document_version,
        )

        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_can_create_record_for_each_defined_status(self):
        for index, status in enumerate(ImplementationRecordStatus.values, start=1):
            with self.subTest(status=status):
                user = get_user_model().objects.create_user(
                    email=f"lector{index}@example.com",
                    password="test-pass",
                )
                record = self.create_implementation_record(user=user, status=status)

                self.assertEqual(record.status, status)
