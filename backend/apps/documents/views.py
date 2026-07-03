from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.views import View
from django.views.generic import DetailView, ListView

from apps.audit.services import AuditContext
from config.access import ModuleAccessMixin
from config.navigation import can_access_documents_module

from .models import Document, DocumentStatus
from .permissions import can_view_document_file, can_view_obsolete_document
from .selectors import (
    document_detail_queryset,
    document_file_get_for_controlled_delivery,
    document_list,
    document_version_list,
)
from .services import (
    document_file_access_denied_audit_create,
    document_file_access_granted_audit_create,
)


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


class ControlledDocumentFileView(LoginRequiredMixin, View):
    content_type = "application/pdf"

    def get_audit_context(self):
        return AuditContext(
            user=self.request.user,
            ip_address=self.request.META.get("REMOTE_ADDR"),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

    def get_document_file(self):
        document_file = document_file_get_for_controlled_delivery(
            document_id=self.kwargs["document_id"],
            version_id=self.kwargs["version_id"],
            file_id=self.kwargs["file_id"],
        )
        if document_file is None:
            raise Http404("Document file not found.")
        return document_file

    def get(self, request, *args, **kwargs):
        document_file = self.get_document_file()
        audit_context = self.get_audit_context()

        if not can_view_document_file(request.user, document_file):
            document_file_access_denied_audit_create(
                document_file=document_file,
                audit_context=audit_context,
            )
            raise PermissionDenied("You do not have permission to view this document file.")

        try:
            file_handle = document_file.file.open("rb")
        except OSError as exc:
            raise Http404("Document file not found.") from exc

        document_file_access_granted_audit_create(
            document_file=document_file,
            audit_context=audit_context,
        )
        response = FileResponse(
            file_handle,
            as_attachment=False,
            filename=document_file.original_filename,
            content_type=self.content_type,
        )
        response["Cache-Control"] = "no-store"
        response["Pragma"] = "no-cache"
        response["X-Content-Type-Options"] = "nosniff"
        return response
