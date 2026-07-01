from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from config.access import ModuleAccessMixin
from config.navigation import can_access_document_requests_module, get_module_navigation

from .forms import DocumentRequestCreateForm
from .models import DocumentRequest
from .permissions import can_create_document_request, can_view_all_document_requests
from .selectors import document_request_list


class DocumentRequestAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_access_document_requests_module)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module_navigation"] = get_module_navigation(self.request.user)
        context["can_create_document_request"] = can_create_document_request(
            self.request.user,
        )
        return context


class DocumentRequestListView(DocumentRequestAccessMixin, ListView):
    template_name = "document_requests/document_request_list.html"
    context_object_name = "document_requests"

    def get_queryset(self):
        if can_view_all_document_requests(self.request.user):
            return document_request_list()
        return document_request_list(requested_by=self.request.user)


class DocumentRequestDetailView(DocumentRequestAccessMixin, DetailView):
    model = DocumentRequest
    template_name = "document_requests/document_request_detail.html"
    context_object_name = "document_request"

    def get_queryset(self):
        if can_view_all_document_requests(self.request.user):
            return document_request_list()
        return document_request_list(requested_by=self.request.user)


class DocumentRequestCreateView(DocumentRequestAccessMixin, CreateView):
    form_class = DocumentRequestCreateForm
    template_name = "document_requests/document_request_form.html"
    permission_check = staticmethod(can_create_document_request)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("app:document_requests:detail", args=[self.object.pk])
