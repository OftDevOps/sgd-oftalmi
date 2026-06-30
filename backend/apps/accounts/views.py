from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from config.access import ModuleIndexView

from .permissions import can_view_users
from .redirects import get_role_home_url


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_url = self.get_redirect_url()
        if redirect_url:
            return redirect_url

        return get_role_home_url(self.request.user)


class LoggedOutView(TemplateView):
    template_name = "accounts/logged_out.html"


class AccountsIndexView(ModuleIndexView):
    module_key = "users"
    module_title = "Usuarios"
    module_section = "Administracion"
    permission_check = staticmethod(can_view_users)
