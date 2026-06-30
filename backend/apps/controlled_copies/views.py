from config.access import ModuleIndexView

from .permissions import can_view_controlled_copies


class ControlledCopyIndexView(ModuleIndexView):
    module_key = "controlled_copies"
    module_title = "Copias controladas"
    module_section = "Gestion documental"
    permission_check = staticmethod(can_view_controlled_copies)
