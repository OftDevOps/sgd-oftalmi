from django.views.generic import DetailView, ListView

from config.access import ModuleAccessMixin

from .models import OrganizationalUnit
from .permissions import can_view_organizational_units
from .selectors import organizational_unit_list


class OrganizationalUnitAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_organizational_units)


class OrganizationalUnitListView(OrganizationalUnitAccessMixin, ListView):
    template_name = "catalogs/organizational_unit_list.html"
    context_object_name = "organizational_units"

    def get_queryset(self):
        return organizational_unit_list()


class OrganizationalUnitDetailView(OrganizationalUnitAccessMixin, DetailView):
    model = OrganizationalUnit
    template_name = "catalogs/organizational_unit_detail.html"
    context_object_name = "organizational_unit"

    def get_queryset(self):
        return organizational_unit_list()
