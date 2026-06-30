from django.urls import reverse

from apps.accounts.models import UserRole
from apps.accounts.permissions import (
    can_view_users,
    has_any_role,
    is_active_user,
)
from apps.audit.permissions import can_view_audit
from apps.controlled_copies.permissions import can_view_controlled_copies
from apps.document_requests.permissions import (
    can_create_document_request,
    can_view_all_document_requests,
)
from apps.document_types.permissions import can_view_document_types
from apps.implementation_records.permissions import (
    can_report_pending_implementation_records,
)
from apps.notifications.permissions import can_view_own_notifications
from apps.organizational_units.permissions import can_view_organizational_units
from apps.reports.permissions import can_view_reports


def can_access_documents_module(user):
    return has_any_role(
        user,
        {
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        },
    )


def can_access_document_requests_module(user):
    return can_create_document_request(user) or can_view_all_document_requests(user)


def can_access_implementation_records_module(user):
    return is_active_user(user) or can_report_pending_implementation_records(user)


MODULE_GROUPS = (
    {
        "title": "Administracion",
        "items": (
            {
                "key": "users",
                "label": "Usuarios",
                "url_name": "app:accounts:index",
                "permission": can_view_users,
            },
            {
                "key": "organizational_units",
                "label": "Unidades ejecutoras",
                "url_name": "app:organizational_units:index",
                "permission": can_view_organizational_units,
            },
            {
                "key": "document_types",
                "label": "Tipos documentales",
                "url_name": "app:document_types:index",
                "permission": can_view_document_types,
            },
        ),
    },
    {
        "title": "Gestion documental",
        "items": (
            {
                "key": "documents",
                "label": "Documentos",
                "url_name": "app:documents:index",
                "permission": can_access_documents_module,
            },
            {
                "key": "document_requests",
                "label": "Solicitudes",
                "url_name": "app:document_requests:index",
                "permission": can_access_document_requests_module,
            },
            {
                "key": "controlled_copies",
                "label": "Copias controladas",
                "url_name": "app:controlled_copies:index",
                "permission": can_view_controlled_copies,
            },
            {
                "key": "implementation_records",
                "label": "Constancias",
                "url_name": "app:implementation_records:index",
                "permission": can_access_implementation_records_module,
            },
        ),
    },
    {
        "title": "Control",
        "items": (
            {
                "key": "audit",
                "label": "Auditoria",
                "url_name": "app:audit:index",
                "permission": can_view_audit,
            },
            {
                "key": "reports",
                "label": "Reportes",
                "url_name": "app:reports:index",
                "permission": can_view_reports,
            },
            {
                "key": "notifications",
                "label": "Notificaciones",
                "url_name": "app:notifications:index",
                "permission": can_view_own_notifications,
            },
        ),
    },
)


def get_module_navigation(user):
    navigation = []

    for group in MODULE_GROUPS:
        items = []
        for item in group["items"]:
            if item["permission"](user):
                items.append(
                    {
                        "key": item["key"],
                        "label": item["label"],
                        "url": reverse(item["url_name"]),
                    }
                )

        if items:
            navigation.append({"title": group["title"], "items": items})

    return navigation
