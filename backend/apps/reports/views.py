from django.views.generic import ListView

from config.access import ModuleAccessMixin, ModuleIndexView

from .forms import MasterBookFilterForm
from .permissions import can_view_reports
from .selectors import get_master_book_queryset


class ReportAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_reports)


class ReportIndexView(ModuleIndexView):
    module_key = "reports"
    module_title = "Reportes"
    module_section = "Control"
    permission_check = staticmethod(can_view_reports)


class MasterBookView(ReportAccessMixin, ListView):
    template_name = "reports/master_book.html"
    context_object_name = "documents"

    def get_filter_form(self):
        return MasterBookFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        if not self.filter_form.is_valid():
            return get_master_book_queryset()

        filters = {
            key: value
            for key, value in self.filter_form.cleaned_data.items()
            if value not in (None, "")
        }
        if "date_from" in filters or "date_to" in filters:
            filters["date_field"] = "created_at__date"
        return get_master_book_queryset(**filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        return context
