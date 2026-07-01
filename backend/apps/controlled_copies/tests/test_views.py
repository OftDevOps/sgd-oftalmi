from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.controlled_copies.models import ControlledCopy, ControlledCopyStatus
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentVersion
from apps.organizational_units.models import OrganizationalUnit


class ControlledCopyViewsTests(TestCase):
    def create_user(self, role, prefix, organizational_unit=None):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
            organizational_unit=organizational_unit,
        )

    def create_controlled_copy(
        self,
        *,
        copy_number,
        receiver_unit,
        receiver_user=None,
        status=ControlledCopyStatus.ACTIVE,
    ):
        return ControlledCopy.objects.create(
            document=self.document,
            document_version=self.document_version,
            copy_number=copy_number,
            receiver_unit=receiver_unit,
            receiver_user=receiver_user,
            status=status,
            observations=f"Observacion {copy_number}",
            evidence_reference=f"ACTA-{copy_number}",
            created_by=self.oym_admin,
        )

    def setUp(self):
        self.oym_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.production_unit = OrganizationalUnit.objects.create(
            name="Produccion",
            code="PROD",
        )
        self.quality_unit = OrganizationalUnit.objects.create(
            name="Garantia de Calidad",
            code="GC",
        )
        self.oym_admin = self.create_user(
            UserRole.OYM_ADMIN,
            "oym-admin",
            organizational_unit=self.oym_unit,
        )
        self.production_user = self.create_user(
            UserRole.EXECUTING_UNIT,
            "production",
            organizational_unit=self.production_unit,
        )
        self.reader_user = self.create_user(
            UserRole.READER,
            "reader",
            organizational_unit=self.quality_unit,
        )
        self.systems_user = self.create_user(
            UserRole.SYSTEMS_TECH_ADMIN,
            "systems",
            organizational_unit=self.oym_unit,
        )
        self.auditor_user = self.create_user(UserRole.AUDITOR, "auditor")
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro de Copias Controladas",
            document_type=self.document_type,
            owner_unit=self.oym_unit,
            created_by=self.oym_admin,
        )
        self.document_version = DocumentVersion.objects.create(
            document=self.document,
            version_number="01",
            created_by=self.oym_admin,
        )
        self.unit_copy = self.create_controlled_copy(
            copy_number="CC-001",
            receiver_unit=self.production_unit,
        )
        self.user_copy = self.create_controlled_copy(
            copy_number="CC-002",
            receiver_unit=self.quality_unit,
            receiver_user=self.reader_user,
        )
        self.other_user_copy = self.create_controlled_copy(
            copy_number="CC-003",
            receiver_unit=self.production_unit,
            receiver_user=self.create_user(
                UserRole.READER,
                "other-reader",
                organizational_unit=self.production_unit,
            ),
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:controlled_copies:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_oym_can_view_all_controlled_copies(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(reverse("app:controlled_copies:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CC-001")
        self.assertContains(response, "CC-002")
        self.assertContains(response, "CC-003")

    def test_receiver_unit_can_view_unit_copies_only(self):
        self.client.force_login(self.production_user)

        response = self.client.get(reverse("app:controlled_copies:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CC-001")
        self.assertNotContains(response, "CC-002")
        self.assertNotContains(response, "CC-003")

    def test_receiver_user_can_view_user_copy(self):
        self.client.force_login(self.reader_user)

        response = self.client.get(reverse("app:controlled_copies:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CC-002")
        self.assertNotContains(response, "CC-001")
        self.assertNotContains(response, "CC-003")

    def test_systems_and_auditor_cannot_access_list_without_helper_permission(self):
        for user in (self.systems_user, self.auditor_user):
            with self.subTest(user=user.email):
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(reverse("app:controlled_copies:index"))

                self.assertEqual(response.status_code, 403)

    def test_oym_can_view_controlled_copy_detail(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:controlled_copies:detail", args=[self.unit_copy.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001 - copia CC-001")
        self.assertContains(response, "Observacion CC-001")
        self.assertContains(response, "ACTA-CC-001")

    def test_receiver_unit_can_view_unit_copy_detail(self):
        self.client.force_login(self.production_user)

        response = self.client.get(
            reverse("app:controlled_copies:detail", args=[self.unit_copy.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CC-001")

    def test_receiver_cannot_view_unassigned_copy_detail(self):
        self.client.force_login(self.reader_user)

        response = self.client.get(
            reverse("app:controlled_copies:detail", args=[self.unit_copy.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_no_public_create_route_is_exposed(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get("/app/controlled-copies/new/")

        self.assertEqual(response.status_code, 404)
