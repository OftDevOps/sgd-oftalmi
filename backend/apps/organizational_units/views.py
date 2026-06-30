from config.access import ModuleIndexView

from .permissions import can_view_organizational_units


class OrganizationalUnitIndexView(ModuleIndexView):
    module_key = "organizational_units"
    module_title = "Unidades ejecutoras"
    module_section = "Administracion"
    permission_check = staticmethod(can_view_organizational_units)
