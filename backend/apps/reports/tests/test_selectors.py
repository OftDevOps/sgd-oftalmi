from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.controlled_copies.models import ControlledCopy, ControlledCopyStatus
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentStatus, DocumentVersion
from apps.implementation_records.models import ImplementationRecord, ImplementationRecordStatus
from apps.organizational_units.models import OrganizationalUnit

from apps.reports.selectors import (
    get_controlled_copies_report_queryset,
    get_implementation_records_report_queryset,
    get_master_book_queryset,
    get_monthly_document_report_queryset,
)


class ReportsSelectorsTests(TestCase):
    def setUp(self):
        self.oym_user = get_user_model().objects.create_user(
            email="oym@oftalmi.test",
            password="test-pass",
        )
        self.reader = get_user_model().objects.create_user(
            email="lector@oftalmi.test",
            password="test-pass",
        )
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.other_document_type = DocumentType.objects.create(code="INS", name="Instructivo")
        self.owner_unit = OrganizationalUnit.objects.create(name="OyM", code="OYM")
        self.receiver_unit = OrganizationalUnit.objects.create(name="Produccion", code="PROD")

        self.reference_datetime = timezone.now().replace(microsecond=0)
        self.date_from = self.reference_datetime - timedelta(days=1)
        self.date_to = self.reference_datetime + timedelta(days=1)

        self.master_document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro principal",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_user,
            status=DocumentStatus.ACTIVE,
        )
        self.master_version = DocumentVersion.objects.create(
            document=self.master_document,
            version_number="01",
            status=DocumentStatus.ACTIVE,
            issue_date=self.reference_datetime.date(),
            effective_date=self.reference_datetime.date(),
            published_at=self.reference_datetime,
            created_by=self.oym_user,
        )
        Document.objects.filter(pk=self.master_document.pk).update(
            current_version_id=self.master_version.pk,
            updated_at=self.reference_datetime,
        )

        self.monthly_document = Document.objects.create(
            code="INS-OYM-001",
            title="Registro mensual",
            document_type=self.other_document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_user,
            status=DocumentStatus.PUBLISHED,
        )
        self.monthly_version = DocumentVersion.objects.create(
            document=self.monthly_document,
            version_number="02",
            status=DocumentStatus.PUBLISHED,
            issue_date=self.reference_datetime.date(),
            effective_date=self.reference_datetime.date(),
            published_at=self.reference_datetime,
            created_by=self.oym_user,
        )
        Document.objects.filter(pk=self.monthly_document.pk).update(
            current_version_id=self.monthly_version.pk,
            updated_at=self.reference_datetime,
        )

        self.controlled_copy = ControlledCopy.objects.create(
            document=self.master_document,
            document_version=self.master_version,
            copy_number="CC-001",
            receiver_unit=self.receiver_unit,
            receiver_user=self.reader,
            delivered_at=self.reference_datetime,
            status=ControlledCopyStatus.ACTIVE,
            created_by=self.oym_user,
        )
        ControlledCopy.objects.create(
            document=self.monthly_document,
            document_version=self.monthly_version,
            copy_number="CC-002",
            receiver_unit=self.owner_unit,
            status=ControlledCopyStatus.RETIRED,
            retired_at=self.reference_datetime,
            created_by=self.oym_user,
        )

        self.implementation_record = ImplementationRecord.objects.create(
            user=self.reader,
            document=self.master_document,
            document_version=self.master_version,
            assigned_at=self.reference_datetime,
            status=ImplementationRecordStatus.PENDING,
        )
        ImplementationRecord.objects.create(
            user=self.oym_user,
            document=self.monthly_document,
            document_version=self.monthly_version,
            assigned_at=self.reference_datetime - timedelta(days=10),
            status=ImplementationRecordStatus.CANCELLED,
        )

    def test_master_book_queryset_filters_and_uses_related_fields(self):
        queryset = get_master_book_queryset(
            document_type=self.document_type,
            organizational_unit=self.owner_unit,
            status=DocumentStatus.ACTIVE,
            code=self.master_document.code,
            version_number=self.master_version.version_number,
            responsible_user=self.oym_user,
            date_field="updated_at",
            date_from=self.date_from,
            date_to=self.date_to,
            vigency="current",
        )

        self.assertEqual(queryset.model, Document)
        with self.assertNumQueries(1):
            rows = list(queryset)

        self.assertEqual(rows, [self.master_document])
        self.assertEqual(rows[0].document_type, self.document_type)
        self.assertEqual(rows[0].owner_unit, self.owner_unit)
        self.assertEqual(rows[0].current_version, self.master_version)

    def test_monthly_document_report_queryset_filters_by_dates_and_version(self):
        queryset = get_monthly_document_report_queryset(
            document_type=self.other_document_type,
            organizational_unit=self.owner_unit,
            status=DocumentStatus.PUBLISHED,
            code=self.monthly_document.code,
            version_number=self.monthly_version.version_number,
            responsible_user=self.oym_user,
            date_field="published_at",
            date_from=self.date_from,
            date_to=self.date_to,
            vigency="current",
        )

        self.assertEqual(queryset.model, DocumentVersion)
        with self.assertNumQueries(1):
            rows = list(queryset)

        self.assertEqual(rows, [self.monthly_version])
        self.assertEqual(rows[0].document, self.monthly_document)
        self.assertEqual(rows[0].document.document_type, self.other_document_type)
        self.assertEqual(rows[0].document.owner_unit, self.owner_unit)

    def test_controlled_copies_report_queryset_filters_receiver_and_status(self):
        queryset = get_controlled_copies_report_queryset(
            document_type=self.document_type,
            organizational_unit=self.owner_unit,
            status=ControlledCopyStatus.ACTIVE,
            code=self.master_document.code,
            version_number=self.master_version.version_number,
            receiver_unit=self.receiver_unit,
            receiver_user=self.reader,
            responsible_user=self.oym_user,
            date_field="delivered_at",
            date_from=self.date_from,
            date_to=self.date_to,
            vigency="current",
        )

        self.assertEqual(queryset.model, ControlledCopy)
        with self.assertNumQueries(1):
            rows = list(queryset)

        self.assertEqual(rows, [self.controlled_copy])
        self.assertEqual(rows[0].document, self.master_document)
        self.assertEqual(rows[0].document.document_type, self.document_type)
        self.assertEqual(rows[0].receiver_unit, self.receiver_unit)
        self.assertEqual(rows[0].receiver_user, self.reader)

    def test_implementation_records_report_queryset_filters_user_and_date_range(self):
        queryset = get_implementation_records_report_queryset(
            document_type=self.document_type,
            organizational_unit=self.owner_unit,
            status=ImplementationRecordStatus.PENDING,
            code=self.master_document.code,
            version_number=self.master_version.version_number,
            user=self.reader,
            date_field="assigned_at",
            date_from=self.date_from,
            date_to=self.date_to,
            vigency="current",
        )

        self.assertEqual(queryset.model, ImplementationRecord)
        with self.assertNumQueries(1):
            rows = list(queryset)

        self.assertEqual(rows, [self.implementation_record])
        self.assertEqual(rows[0].document, self.master_document)
        self.assertEqual(rows[0].document.document_type, self.document_type)
        self.assertEqual(rows[0].user, self.reader)

    def test_selectors_return_no_rows_for_invalid_date_range(self):
        queryset = get_master_book_queryset(
            date_field="updated_at",
            date_from=self.date_to,
            date_to=self.date_from,
        )

        self.assertEqual(list(queryset), [])
