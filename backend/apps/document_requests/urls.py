from django.urls import path

from .views import DocumentRequestIndexView


app_name = "document_requests"

urlpatterns = [
    path("", DocumentRequestIndexView.as_view(), name="index"),
]
