from django.views.generic import DetailView, ListView

from config.access import ModuleAccessMixin

from .models import DocumentType
from .permissions import can_view_document_types
from .selectors import document_type_list


class DocumentTypeAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_document_types)


class DocumentTypeListView(DocumentTypeAccessMixin, ListView):
    template_name = "catalogs/document_type_list.html"
    context_object_name = "document_types"

    def get_queryset(self):
        return document_type_list()


class DocumentTypeDetailView(DocumentTypeAccessMixin, DetailView):
    model = DocumentType
    template_name = "catalogs/document_type_detail.html"
    context_object_name = "document_type"

    def get_queryset(self):
        return document_type_list()
