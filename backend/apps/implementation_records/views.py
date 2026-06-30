from config.access import ModuleIndexView
from config.navigation import can_access_implementation_records_module


class ImplementationRecordIndexView(ModuleIndexView):
    module_key = "implementation_records"
    module_title = "Constancias"
    module_section = "Gestion documental"
    permission_check = staticmethod(can_access_implementation_records_module)
