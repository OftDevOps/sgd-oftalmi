from django.views.generic import ListView

from config.access import ModuleAccessMixin, ModuleIndexView

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

    def get_queryset(self):
        return get_master_book_queryset()
