from django.test import TestCase

from apps.organizational_units.selectors import (
    organizational_unit_get_by_code,
    organizational_unit_list,
)
from apps.organizational_units.services import organizational_unit_create


class OrganizationalUnitServicesSelectorsTests(TestCase):
    def test_create_and_filter_organizational_unit(self):
        active_unit = organizational_unit_create(name="Produccion", code="PROD")
        organizational_unit_create(name="Inactiva", code="INAC", is_active=False)

        self.assertEqual(organizational_unit_get_by_code("PROD"), active_unit)
        self.assertEqual(list(organizational_unit_list(is_active=True)), [active_unit])
