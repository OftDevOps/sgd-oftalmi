from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.organizational_units.models import OrganizationalUnit


class OrganizationalUnitModelTests(TestCase):
    def test_create_organizational_unit_with_name(self):
        unit = OrganizationalUnit.objects.create(name="Organizacion y Metodos")

        self.assertEqual(unit.name, "Organizacion y Metodos")
        self.assertIsNone(unit.code)

    def test_string_representation(self):
        unit = OrganizationalUnit.objects.create(name="Sistemas", code="SIS")

        self.assertEqual(str(unit), "Sistemas")

    def test_is_active_defaults_to_true(self):
        unit = OrganizationalUnit.objects.create(name="Produccion")

        self.assertTrue(unit.is_active)

    def test_code_is_unique_when_provided(self):
        OrganizationalUnit.objects.create(name="Recursos Humanos", code="RRHH")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                OrganizationalUnit.objects.create(name="Talento Humano", code="RRHH")
