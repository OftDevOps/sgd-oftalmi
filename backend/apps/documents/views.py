from django.views.generic import DetailView, ListView

from config.access import ModuleAccessMixin
from config.navigation import can_access_documents_module

from .models import Document, DocumentStatus
from .permissions import can_view_obsolete_document
from .selectors import document_detail_queryset, document_list, document_version_list


VISIBLE_DOCUMENT_STATUSES = {
    DocumentStatus.PUBLISHED,
    DocumentStatus.ACTIVE,
}


class DocumentAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_access_documents_module)


class DocumentListView(DocumentAccessMixin, ListView):
    template_name = "documents/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        queryset = document_detail_queryset()
        if not can_view_obsolete_document(self.request.user):
            queryset = queryset.filter(status__in=VISIBLE_DOCUMENT_STATUSES)
        return queryset


class DocumentDetailView(DocumentAccessMixin, DetailView):
    model = Document
    template_name = "documents/document_detail.html"
    context_object_name = "document"

    def get_queryset(self):
        queryset = document_list()
        if not can_view_obsolete_document(self.request.user):
            queryset = queryset.filter(status__in=VISIBLE_DOCUMENT_STATUSES)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        versions = document_version_list(document=self.object).prefetch_related(
            "files__uploaded_by",
        )

        if not can_view_obsolete_document(self.request.user):
            versions = versions.filter(status__in=VISIBLE_DOCUMENT_STATUSES)

        context["document_versions"] = versions
        return context
