from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from .navigation import get_module_navigation


class ModuleAccessMixin(LoginRequiredMixin):
    permission_check = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        permission_check = self.__class__.permission_check
        if permission_check is not None and not permission_check(request.user):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("module_navigation", get_module_navigation(self.request.user))
        return context


class ModuleIndexView(ModuleAccessMixin, TemplateView):
    template_name = "app/module_index.html"
    module_key = ""
    module_title = ""
    module_section = ""
    module_status = "Base de acceso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "module_key": self.module_key,
                "module_title": self.module_title,
                "module_section": self.module_section,
                "module_status": self.module_status,
            }
        )
        return context
