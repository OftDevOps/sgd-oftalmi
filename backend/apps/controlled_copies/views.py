from django.db.models import Q
from django.views.generic import DetailView, ListView

from apps.accounts.permissions import is_oym_user
from config.access import ModuleAccessMixin
from config.navigation import get_module_navigation

from .models import ControlledCopy
from .permissions import can_view_controlled_copies
from .selectors import controlled_copy_list


class ControlledCopyAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_controlled_copies)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module_navigation"] = get_module_navigation(self.request.user)
        return context


class ControlledCopyQuerysetMixin:
    def get_queryset(self):
        queryset = controlled_copy_list()
        user = self.request.user

        if is_oym_user(user):
            return queryset

        visibility_filter = Q(receiver_user=user)
        if user.organizational_unit_id:
            visibility_filter |= Q(
                receiver_user__isnull=True,
                receiver_unit=user.organizational_unit,
            )

        return queryset.filter(visibility_filter)


class ControlledCopyListView(
    ControlledCopyAccessMixin,
    ControlledCopyQuerysetMixin,
    ListView,
):
    template_name = "controlled_copies/controlled_copy_list.html"
    context_object_name = "controlled_copies"


class ControlledCopyDetailView(
    ControlledCopyAccessMixin,
    ControlledCopyQuerysetMixin,
    DetailView,
):
    model = ControlledCopy
    template_name = "controlled_copies/controlled_copy_detail.html"
    context_object_name = "controlled_copy"
