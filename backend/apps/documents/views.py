from config.access import ModuleIndexView
from config.navigation import can_access_documents_module


class DocumentIndexView(ModuleIndexView):
    module_key = "documents"
    module_title = "Documentos"
    module_section = "Gestion documental"
    permission_check = staticmethod(can_access_documents_module)
