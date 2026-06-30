from config.access import ModuleIndexView
from config.navigation import can_access_document_requests_module


class DocumentRequestIndexView(ModuleIndexView):
    module_key = "document_requests"
    module_title = "Solicitudes documentales"
    module_section = "Gestion documental"
    permission_check = staticmethod(can_access_document_requests_module)
