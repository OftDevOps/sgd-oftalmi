import tempfile
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings

from apps.accounts.models import ROLE_GROUP_NAMES
from apps.controlled_copies.models import ControlledCopy
from apps.documents.models import Document, DocumentFile
from apps.implementation_records.models import ImplementationRecord
from apps.reports.management.commands.seed_pilot_demo_data import (
    DEMO_CONTROLLED_COPIES,
    DEMO_DOCUMENTS,
    DEMO_IMPLEMENTATION_RECORDS,
    DEMO_USERS,
)
from apps.reports.selectors import (
    get_controlled_copies_report_queryset,
    get_implementation_records_report_queryset,
    get_master_book_queryset,
    get_monthly_document_report_queryset,
)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class SeedPilotDemoDataCommandTests(TestCase):
    def setUp(self):
        for group_name in ROLE_GROUP_NAMES.values():
            Group.objects.get_or_create(name=group_name)

    def call_seed_command(self, **options):
        output = StringIO()
        call_command("seed_pilot_demo_data", stdout=output, **options)
        return output.getvalue()

    def test_seed_creates_demo_users_documents_copies_and_records(self):
        output = self.call_seed_command()

        self.assertIn("Pilot demo seed completed", output)
        self.assertEqual(get_user_model().objects.count(), len(DEMO_USERS))
        self.assertEqual(Document.objects.count(), len(DEMO_DOCUMENTS))
        self.assertEqual(DocumentFile.objects.count(), len(DEMO_DOCUMENTS))
        self.assertEqual(ControlledCopy.objects.count(), len(DEMO_CONTROLLED_COPIES))
        self.assertEqual(
            ImplementationRecord.objects.count(),
            len(DEMO_IMPLEMENTATION_RECORDS),
        )
        self.assertTrue(
            get_user_model().objects.filter(
                email="oym.admin.demo@oftalmi.test",
                role="oym_admin",
            ).exists()
        )
        self.assertTrue(Document.objects.filter(code="PROC-OYM-DEMO-001").exists())

    def test_seed_is_idempotent(self):
        self.call_seed_command()
        self.call_seed_command()

        self.assertEqual(get_user_model().objects.count(), len(DEMO_USERS))
        self.assertEqual(Document.objects.count(), len(DEMO_DOCUMENTS))
        self.assertEqual(DocumentFile.objects.count(), len(DEMO_DOCUMENTS))
        self.assertEqual(ControlledCopy.objects.count(), len(DEMO_CONTROLLED_COPIES))
        self.assertEqual(
            ImplementationRecord.objects.count(),
            len(DEMO_IMPLEMENTATION_RECORDS),
        )

    def test_seed_data_feeds_report_selectors(self):
        self.call_seed_command()

        master_codes = set(get_master_book_queryset().values_list("code", flat=True))
        monthly_codes = set(
            get_monthly_document_report_queryset().values_list(
                "document__code",
                flat=True,
            )
        )
        copy_numbers = set(
            get_controlled_copies_report_queryset().values_list(
                "copy_number",
                flat=True,
            )
        )
        implementation_codes = set(
            get_implementation_records_report_queryset().values_list(
                "document__code",
                flat=True,
            )
        )

        self.assertIn("PROC-OYM-DEMO-001", master_codes)
        self.assertIn("INST-PROD-DEMO-001", monthly_codes)
        self.assertIn("C-001", copy_numbers)
        self.assertIn("PROC-OYM-DEMO-001", implementation_codes)

    def test_seed_uses_only_fictitious_demo_identifiers(self):
        self.call_seed_command()

        self.assertTrue(
            all(
                email.endswith("@oftalmi.test")
                for email in get_user_model().objects.values_list("email", flat=True)
            )
        )
        self.assertTrue(
            all(
                "demo" in title.lower()
                for title in Document.objects.values_list("title", flat=True)
            )
        )
        self.assertFalse(
            DocumentFile.objects.filter(file__icontains="MEDIA_URL").exists()
        )

    def test_seed_fails_when_base_role_groups_are_missing(self):
        Group.objects.all().delete()

        with self.assertRaisesMessage(CommandError, "Missing base role groups"):
            self.call_seed_command()
