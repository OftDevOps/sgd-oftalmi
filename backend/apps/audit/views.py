from django.views.generic import DetailView, ListView

from config.access import ModuleAccessMixin
from config.navigation import get_module_navigation

from .models import AuditEvent
from .permissions import can_view_audit
from .selectors import audit_event_list


class AuditAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_audit)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module_navigation"] = get_module_navigation(self.request.user)
        return context


class AuditEventListView(AuditAccessMixin, ListView):
    template_name = "audit/audit_event_list.html"
    context_object_name = "audit_events"

    def get_queryset(self):
        return audit_event_list()


class AuditEventDetailView(AuditAccessMixin, DetailView):
    model = AuditEvent
    template_name = "audit/audit_event_detail.html"
    context_object_name = "audit_event"

    def get_queryset(self):
        return audit_event_list()
