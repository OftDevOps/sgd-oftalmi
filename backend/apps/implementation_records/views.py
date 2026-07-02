from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from apps.accounts.permissions import is_active_user
from config.access import ModuleAccessMixin
from config.navigation import can_access_implementation_records_module

from .forms import ImplementationRecordCreateForm
from .models import ImplementationRecord
from .permissions import can_view_implementation_records_by_document
from .selectors import implementation_record_list


class ImplementationRecordAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_access_implementation_records_module)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_implementation_record"] = is_active_user(self.request.user)
        return context


class ImplementationRecordQuerysetMixin:
    def get_queryset(self):
        if can_view_implementation_records_by_document(self.request.user):
            return implementation_record_list()
        return implementation_record_list(user=self.request.user)


class ImplementationRecordListView(
    ImplementationRecordAccessMixin,
    ImplementationRecordQuerysetMixin,
    ListView,
):
    template_name = "implementation_records/implementation_record_list.html"
    context_object_name = "implementation_records"


class ImplementationRecordDetailView(
    ImplementationRecordAccessMixin,
    ImplementationRecordQuerysetMixin,
    DetailView,
):
    model = ImplementationRecord
    template_name = "implementation_records/implementation_record_detail.html"
    context_object_name = "implementation_record"


class ImplementationRecordCreateView(ImplementationRecordAccessMixin, CreateView):
    form_class = ImplementationRecordCreateForm
    template_name = "implementation_records/implementation_record_form.html"
    permission_check = staticmethod(is_active_user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("app:implementation_records:detail", args=[self.object.pk])
