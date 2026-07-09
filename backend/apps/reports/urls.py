from django.urls import path

from .views import (
    ControlledCopiesReportExportView,
    ControlledCopiesReportView,
    ImplementationRecordsReportExportView,
    ImplementationRecordsReportView,
    MasterBookExportView,
    MasterBookView,
    MonthlyDocumentReportExportView,
    MonthlyDocumentReportView,
    ReportIndexView,
)


app_name = "reports"

urlpatterns = [
    path("", ReportIndexView.as_view(), name="index"),
    path("master-book/", MasterBookView.as_view(), name="master_book"),
    path(
        "master-book/export.csv",
        MasterBookExportView.as_view(),
        name="master_book_export",
    ),
    path(
        "monthly-documents/",
        MonthlyDocumentReportView.as_view(),
        name="monthly_documents",
    ),
    path(
        "monthly-documents/export.csv",
        MonthlyDocumentReportExportView.as_view(),
        name="monthly_documents_export",
    ),
    path(
        "controlled-copies/",
        ControlledCopiesReportView.as_view(),
        name="controlled_copies",
    ),
    path(
        "controlled-copies/export.csv",
        ControlledCopiesReportExportView.as_view(),
        name="controlled_copies_export",
    ),
    path(
        "implementation-records/",
        ImplementationRecordsReportView.as_view(),
        name="implementation_records",
    ),
    path(
        "implementation-records/export.csv",
        ImplementationRecordsReportExportView.as_view(),
        name="implementation_records_export",
    ),
]
