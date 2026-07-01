from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.document_requests.models import (
    DocumentRequest,
    DocumentRequestStatus,
    DocumentRequestType,
)
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentStatus
from apps.organizational_units.models import OrganizationalUnit


class DocumentRequestViewsTests(TestCase):
    def create_user(self, role, prefix, organizational_unit=None):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
            organizational_unit=organizational_unit,
        )

    def create_request(self, *, requested_by, title):
        return DocumentRequest.objects.create(
            request_type=DocumentRequestType.CREATE,
            title=title,
            description="Solicitud base.",
            requested_by=requested_by,
            organizational_unit=requested_by.organizational_unit,
            document_type=self.document_type,
            related_document=self.document,
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
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.oym_admin = self.create_user(
            UserRole.OYM_ADMIN,
            "oym-admin",
            organizational_unit=self.oym_unit,
        )
        self.executing_user = self.create_user(
            UserRole.EXECUTING_UNIT,
            "executing-unit",
            organizational_unit=self.production_unit,
        )
        self.other_user = self.create_user(
            UserRole.EXECUTING_UNIT,
            "other-unit",
            organizational_unit=self.oym_unit,
        )
        self.reader = self.create_user(UserRole.READER, "reader")
        self.document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro documental",
            document_type=self.document_type,
            owner_unit=self.oym_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.ACTIVE,
        )
        self.own_request = self.create_request(
            requested_by=self.executing_user,
            title="Solicitud propia",
        )
        self.other_request = self.create_request(
            requested_by=self.other_user,
            title="Solicitud de otra unidad",
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:document_requests:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_oym_can_view_all_document_requests(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(reverse("app:document_requests:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solicitud propia")
        self.assertContains(response, "Solicitud de otra unidad")
        self.assertContains(response, "Nueva solicitud")

    def test_executing_unit_sees_only_own_document_requests(self):
        self.client.force_login(self.executing_user)

        response = self.client.get(reverse("app:document_requests:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solicitud propia")
        self.assertNotContains(response, "Solicitud de otra unidad")

    def test_reader_cannot_access_document_requests(self):
        self.client.force_login(self.reader)

        response = self.client.get(reverse("app:document_requests:index"))

        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_detail(self):
        self.client.force_login(self.executing_user)

        response = self.client.get(
            reverse("app:document_requests:detail", args=[self.own_request.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solicitud propia")
        self.assertContains(response, "Solicitud base.")
        self.assertContains(response, "FOR-OYM-001 - Registro documental")

    def test_non_oym_user_cannot_view_other_user_detail(self):
        self.client.force_login(self.executing_user)

        response = self.client.get(
            reverse("app:document_requests:detail", args=[self.other_request.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_create_requires_login(self):
        response = self.client.get(reverse("app:document_requests:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_reader_cannot_create_document_request(self):
        self.client.force_login(self.reader)

        response = self.client.get(reverse("app:document_requests:create"))

        self.assertEqual(response.status_code, 403)

    def test_executing_unit_can_create_document_request(self):
        self.client.force_login(self.executing_user)

        response = self.client.post(
            reverse("app:document_requests:create"),
            {
                "request_type": DocumentRequestType.MODIFY,
                "title": "Modificar registro documental",
                "description": "Actualizar datos del documento.",
                "organizational_unit": self.production_unit.pk,
                "document_type": self.document_type.pk,
                "related_document": self.document.pk,
            },
        )

        created_request = DocumentRequest.objects.get(title="Modificar registro documental")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("app:document_requests:detail", args=[created_request.pk]),
        )
        self.assertEqual(created_request.requested_by, self.executing_user)
        self.assertEqual(created_request.organizational_unit, self.production_unit)
        self.assertEqual(created_request.status, DocumentRequestStatus.DRAFT)
        self.assertIsNone(created_request.submitted_at)

    def test_create_form_allows_optional_document_type_and_related_document(self):
        self.client.force_login(self.executing_user)

        response = self.client.post(
            reverse("app:document_requests:create"),
            {
                "request_type": DocumentRequestType.OTHER,
                "title": "Solicitud general",
                "description": "",
                "organizational_unit": self.production_unit.pk,
                "document_type": "",
                "related_document": "",
            },
        )

        created_request = DocumentRequest.objects.get(title="Solicitud general")
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(created_request.document_type)
        self.assertIsNone(created_request.related_document)
