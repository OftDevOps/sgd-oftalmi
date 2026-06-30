from django.urls import path

from .views import DocumentTypeIndexView


app_name = "document_types"

urlpatterns = [
    path("", DocumentTypeIndexView.as_view(), name="index"),
]
