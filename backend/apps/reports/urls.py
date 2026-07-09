from django.urls import path

from .views import (
    ControlledCopiesReportView,
    MasterBookView,
    MonthlyDocumentReportView,
    ReportIndexView,
)


app_name = "reports"

urlpatterns = [
    path("", ReportIndexView.as_view(), name="index"),
    path("master-book/", MasterBookView.as_view(), name="master_book"),
    path(
        "monthly-documents/",
        MonthlyDocumentReportView.as_view(),
        name="monthly_documents",
    ),
    path(
        "controlled-copies/",
        ControlledCopiesReportView.as_view(),
        name="controlled_copies",
    ),
]
