from django.test import TestCase

from apps.document_types.selectors import document_type_get_by_code, document_type_list
from apps.document_types.services import document_type_create


class DocumentTypeServicesSelectorsTests(TestCase):
    def test_create_and_filter_document_type(self):
        active_type = document_type_create(code="FOR", name="Formato")
        document_type_create(code="INS", name="Instructivo", is_active=False)

        self.assertEqual(document_type_get_by_code("FOR"), active_type)
        self.assertEqual(list(document_type_list(is_active=True)), [active_type])
