from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .navigation import get_module_navigation


def root_redirect(request):
    return redirect("app:dashboard")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "app/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module_navigation"] = get_module_navigation(self.request.user)
        return context


def api_v1_index(request):
    if not request.user.is_authenticated:
        return redirect(f"/accounts/login/?next={request.path}")

    return JsonResponse(
        {
            "name": "SGD-OFTALMI internal API",
            "version": "v1",
            "status": "reserved",
            "public": False,
        }
    )
