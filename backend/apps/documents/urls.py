from django.urls import path

from .views import (
    ControlledDocumentFileView,
    ControlledDocumentViewerView,
    DocumentDetailView,
    DocumentListView,
)


app_name = "documents"

urlpatterns = [
    path("", DocumentListView.as_view(), name="index"),
    path(
        "<int:document_id>/versions/<int:version_id>/files/<int:file_id>/viewer/",
        ControlledDocumentViewerView.as_view(),
        name="file_viewer",
    ),
    path(
        "<int:document_id>/versions/<int:version_id>/files/<int:file_id>/view/",
        ControlledDocumentFileView.as_view(),
        name="file_view",
    ),
    path("<int:pk>/", DocumentDetailView.as_view(), name="detail"),
]
