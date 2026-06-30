from config.access import ModuleIndexView

from .permissions import can_view_audit


class AuditIndexView(ModuleIndexView):
    module_key = "audit"
    module_title = "Auditoria"
    module_section = "Control"
    permission_check = staticmethod(can_view_audit)
