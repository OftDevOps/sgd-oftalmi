from config.access import ModuleIndexView

from .permissions import can_view_reports


class ReportIndexView(ModuleIndexView):
    module_key = "reports"
    module_title = "Reportes"
    module_section = "Control"
    permission_check = staticmethod(can_view_reports)
