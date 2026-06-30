from config.access import ModuleIndexView

from .permissions import can_view_own_notifications


class NotificationIndexView(ModuleIndexView):
    module_key = "notifications"
    module_title = "Notificaciones"
    module_section = "Control"
    permission_check = staticmethod(can_view_own_notifications)
