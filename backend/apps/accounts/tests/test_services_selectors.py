from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import UserRole
from apps.accounts.selectors import user_get_by_email, user_list
from apps.accounts.services import user_assign_role, user_set_organizational_unit
from apps.organizational_units.models import OrganizationalUnit


class AccountServicesSelectorsTests(TestCase):
    def test_user_assign_role_syncs_group(self):
        user = get_user_model().objects.create_user(
            email="reader@oftalmi.com",
            password="test-pass",
        )

        user_assign_role(user=user, role=UserRole.OYM_ANALYST)

        self.assertEqual(user.role, UserRole.OYM_ANALYST)
        self.assertTrue(user.groups.filter(name="OYM_ANALYST").exists())

    def test_user_set_organizational_unit_and_selectors(self):
        unit = OrganizationalUnit.objects.create(name="Produccion", code="PROD")
        user = get_user_model().objects.create_user(
            email="reader@oftalmi.com",
            password="test-pass",
        )

        user_set_organizational_unit(user=user, organizational_unit=unit)

        self.assertEqual(user_get_by_email("reader@OFTALMI.COM"), user)
        self.assertEqual(list(user_list(organizational_unit=unit)), [user])
