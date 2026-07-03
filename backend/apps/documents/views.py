from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.audit.services import AuditContext
from config.access import ModuleAccessMixin
from config.navigation import can_access_documents_module, get_module_navigation

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
    document_file_access_failed_audit_create,
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

        for version in versions:
            for document_file in version.files.all():
                document_file.can_open_viewer = can_view_document_file(
                    self.request.user,
                    document_file,
                )

        context["document_versions"] = versions
        return context


class ControlledDocumentViewerView(LoginRequiredMixin, TemplateView):
    template_name = "documents/document_viewer.html"

    def get_audit_context(self):
        return AuditContext(
            user=self.request.user,
            ip_address=self.request.META.get("REMOTE_ADDR"),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

    def get_document_file(self):
        return document_file_get_for_controlled_delivery(
            document_id=self.kwargs["document_id"],
            version_id=self.kwargs["version_id"],
            file_id=self.kwargs["file_id"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_file = self.get_document_file()
        context["module_navigation"] = get_module_navigation(self.request.user)
        context["document_file"] = document_file
        context["can_view_file"] = False
        context["viewer_status"] = 200
        context["viewer_message"] = ""

        if document_file is None:
            context["viewer_status"] = 404
            context["viewer_message"] = "El documento, version o archivo solicitado no existe."
            return context

        context["document_version"] = document_file.document_version
        context["document"] = document_file.document_version.document

        if not can_view_document_file(self.request.user, document_file):
            document_file_access_denied_audit_create(
                document_file=document_file,
                audit_context=self.get_audit_context(),
            )
            context["viewer_status"] = 403
            context["viewer_message"] = "No tiene permiso para visualizar este archivo."
            return context

        if not document_file.file.storage.exists(document_file.file.name):
            document_file_access_failed_audit_create(
                document_file=document_file,
                audit_context=self.get_audit_context(),
            )
            context["viewer_status"] = 404
            context["viewer_message"] = "El archivo documental no esta disponible."
            return context

        context["can_view_file"] = True
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("status", context.get("viewer_status", 200))
        return super().render_to_response(context, **response_kwargs)


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
            document_file_access_failed_audit_create(
                document_file=document_file,
                audit_context=audit_context,
            )
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
