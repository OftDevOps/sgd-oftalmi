from django.urls import reverse

from .models import UserRole


ROLE_DASHBOARDS = {
    UserRole.OYM_ADMIN: {
        "title": "Operacion documental OyM",
        "summary": "Acceso funcional para administrar documentos, solicitudes y control documental.",
        "focus": (
            "Revisar documentos controlados.",
            "Atender solicitudes documentales.",
            "Consultar trazabilidad funcional.",
        ),
        "actions": (
            ("Documentos", "app:documents:index"),
            ("Solicitudes documentales", "app:document_requests:index"),
            ("Copias controladas", "app:controlled_copies:index"),
            ("Constancias", "app:implementation_records:index"),
            ("Auditoria", "app:audit:index"),
        ),
    },
    UserRole.OYM_ANALYST: {
        "title": "Gestion operativa OyM",
        "summary": "Acceso operativo para revisar documentos y dar seguimiento al flujo documental.",
        "focus": (
            "Registrar y revisar solicitudes.",
            "Dar seguimiento a copias controladas.",
            "Revisar constancias pendientes cuando aplique.",
        ),
        "actions": (
            ("Documentos", "app:documents:index"),
            ("Solicitudes documentales", "app:document_requests:index"),
            ("Copias controladas", "app:controlled_copies:index"),
            ("Constancias", "app:implementation_records:index"),
        ),
    },
    UserRole.EXECUTING_UNIT: {
        "title": "Unidad ejecutora",
        "summary": "Acceso para consultar documentos aplicables y gestionar solicitudes propias.",
        "focus": (
            "Consultar documentos asignados o aplicables.",
            "Crear o revisar solicitudes documentales.",
            "Dar seguimiento a implementacion cuando aplique.",
        ),
        "actions": (
            ("Solicitudes documentales", "app:document_requests:index"),
            ("Documentos", "app:documents:index"),
            ("Constancias", "app:implementation_records:index"),
        ),
    },
    UserRole.READER: {
        "title": "Consulta e implementacion",
        "summary": "Acceso de lectura controlada para documentos asignados y constancias propias.",
        "focus": (
            "Consultar documentos asignados o aplicables.",
            "Confirmar lectura, aceptacion e implementacion cuando aplique.",
            "Revisar notificaciones internas.",
        ),
        "actions": (
            ("Documentos", "app:documents:index"),
            ("Constancias", "app:implementation_records:index"),
            ("Notificaciones", "app:notifications:index"),
        ),
    },
    UserRole.SYSTEMS_TECH_ADMIN: {
        "title": "Operacion tecnica",
        "summary": "Acceso tecnico para soporte de plataforma sin asumir reglas funcionales OyM.",
        "focus": (
            "Revisar usuarios segun procedimiento autorizado.",
            "Mantener operacion tecnica y soporte.",
            "Evitar modificar reglas funcionales de OyM.",
        ),
        "actions": (
            ("Usuarios", "app:accounts:index"),
            ("Unidades ejecutoras", "app:organizational_units:index"),
            ("Notificaciones", "app:notifications:index"),
        ),
    },
    UserRole.AUDITOR: {
        "title": "Consulta de auditoria",
        "summary": "Acceso controlado para revisar trazabilidad y eventos autorizados.",
        "focus": (
            "Consultar eventos de auditoria.",
            "Revisar trazabilidad sin modificar registros.",
            "Mantener acceso de solo consulta.",
        ),
        "actions": (
            ("Auditoria", "app:audit:index"),
        ),
    },
}

DEFAULT_DASHBOARD = {
    "title": "Panel interno",
    "summary": "Acceso operativo segun rol y permisos registrados.",
    "focus": (
        "Consultar los modulos disponibles.",
        "Solicitar revision de permisos si falta acceso autorizado.",
    ),
    "actions": (),
}


def get_role_dashboard(user):
    dashboard = ROLE_DASHBOARDS.get(getattr(user, "role", None), DEFAULT_DASHBOARD)

    return {
        "title": dashboard["title"],
        "summary": dashboard["summary"],
        "focus": dashboard["focus"],
        "actions": [
            {
                "label": label,
                "url": reverse(url_name),
            }
            for label, url_name in dashboard["actions"]
        ],
    }
