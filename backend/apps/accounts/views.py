from config.access import ModuleIndexView

from .permissions import can_view_users


class AccountsIndexView(ModuleIndexView):
    module_key = "users"
    module_title = "Usuarios"
    module_section = "Administracion"
    permission_check = staticmethod(can_view_users)
