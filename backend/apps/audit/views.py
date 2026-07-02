from django.views.generic import DetailView, ListView

from config.access import ModuleAccessMixin

from .models import AuditEvent
from .permissions import can_view_audit
from .selectors import audit_event_list


class AuditAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_audit)


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
