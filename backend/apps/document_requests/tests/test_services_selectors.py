from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.document_requests.models import DocumentRequestStatus, DocumentRequestType
from apps.document_requests.selectors import document_request_get_for_user, document_request_list
from apps.document_requests.services import document_request_create
from apps.organizational_units.models import OrganizationalUnit


class DocumentRequestServicesSelectorsTests(TestCase):
    def test_create_document_request_and_filter_by_user(self):
        user = get_user_model().objects.create_user(
            email="solicitante@oftalmi.com",
            password="test-pass",
        )
        unit = OrganizationalUnit.objects.create(name="Produccion", code="PROD")

        request = document_request_create(
            request_type=DocumentRequestType.CREATE,
            title="Solicitud documental",
            requested_by=user,
            organizational_unit=unit,
            status=DocumentRequestStatus.SUBMITTED,
        )

        self.assertEqual(document_request_get_for_user(user=user, document_request_id=request.id), request)
        self.assertEqual(list(document_request_list(status=DocumentRequestStatus.SUBMITTED)), [request])
