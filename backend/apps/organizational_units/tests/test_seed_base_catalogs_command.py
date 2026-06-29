from io import StringIO

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import ROLE_GROUP_NAMES
from apps.document_types.models import DocumentType
from apps.organizational_units.management.commands.seed_base_catalogs import (
    BASE_DOCUMENT_TYPES,
    BASE_ORGANIZATIONAL_UNITS,
)
from apps.organizational_units.models import OrganizationalUnit


class SeedBaseCatalogsCommandTests(TestCase):
    def call_seed_command(self, **options):
        output = StringIO()
        call_command("seed_base_catalogs", stdout=output, **options)
        return output.getvalue()

    def test_seed_creates_base_catalogs_and_role_groups(self):
        Group.objects.filter(name__in=ROLE_GROUP_NAMES.values()).delete()

        output = self.call_seed_command()

        self.assertIn("Seed completed", output)
        self.assertEqual(
            OrganizationalUnit.objects.count(),
            len(BASE_ORGANIZATIONAL_UNITS),
        )
        self.assertEqual(DocumentType.objects.count(), len(BASE_DOCUMENT_TYPES))
        self.assertEqual(
            set(
                Group.objects.filter(name__in=ROLE_GROUP_NAMES.values()).values_list(
                    "name",
                    flat=True,
                )
            ),
            set(ROLE_GROUP_NAMES.values()),
        )

    def test_seed_is_idempotent(self):
        self.call_seed_command()
        self.call_seed_command()

        self.assertEqual(
            OrganizationalUnit.objects.count(),
            len(BASE_ORGANIZATIONAL_UNITS),
        )
        self.assertEqual(DocumentType.objects.count(), len(BASE_DOCUMENT_TYPES))

    def test_seed_updates_existing_catalog_values(self):
        OrganizationalUnit.objects.create(
            code="OYM",
            name="Old name",
            description="Old description",
            is_active=False,
        )
        DocumentType.objects.create(
            code="FOR",
            name="Old type",
            description="Old description",
            is_active=False,
        )

        self.call_seed_command()

        unit = OrganizationalUnit.objects.get(code="OYM")
        document_type = DocumentType.objects.get(code="FOR")

        self.assertEqual(unit.name, "Organizacion y Metodos")
        self.assertTrue(unit.is_active)
        self.assertEqual(document_type.name, "Formato")
        self.assertTrue(document_type.is_active)

    def test_dry_run_does_not_write_catalogs_or_missing_groups(self):
        Group.objects.filter(name__in=ROLE_GROUP_NAMES.values()).delete()

        output = self.call_seed_command(dry_run=True)

        self.assertIn("DRY-RUN", output)
        self.assertFalse(OrganizationalUnit.objects.exists())
        self.assertFalse(DocumentType.objects.exists())
        self.assertFalse(
            Group.objects.filter(name__in=ROLE_GROUP_NAMES.values()).exists()
        )
