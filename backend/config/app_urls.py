from django.urls import include, path

from .views import DashboardView


app_name = "app"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("users/", include("apps.accounts.urls", namespace="accounts")),
    path(
        "catalogs/organizational-units/",
        include("apps.organizational_units.urls", namespace="organizational_units"),
    ),
    path(
        "catalogs/document-types/",
        include("apps.document_types.urls", namespace="document_types"),
    ),
    path("documents/", include("apps.documents.urls", namespace="documents")),
    path(
        "document-requests/",
        include("apps.document_requests.urls", namespace="document_requests"),
    ),
    path(
        "controlled-copies/",
        include("apps.controlled_copies.urls", namespace="controlled_copies"),
    ),
    path(
        "implementation-records/",
        include(
            "apps.implementation_records.urls",
            namespace="implementation_records",
        ),
    ),
    path("audit/", include("apps.audit.urls", namespace="audit")),
    path("reports/", include("apps.reports.urls", namespace="reports")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
]
