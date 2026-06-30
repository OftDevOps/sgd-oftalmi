from config.access import ModuleIndexView

from .permissions import can_view_document_types


class DocumentTypeIndexView(ModuleIndexView):
    module_key = "document_types"
    module_title = "Tipos documentales"
    module_section = "Administracion"
    permission_check = staticmethod(can_view_document_types)
