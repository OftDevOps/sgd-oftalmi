from django.urls import path

from .views import DocumentTypeDetailView, DocumentTypeListView


app_name = "document_types"

urlpatterns = [
    path("", DocumentTypeListView.as_view(), name="index"),
    path("<int:pk>/", DocumentTypeDetailView.as_view(), name="detail"),
]
