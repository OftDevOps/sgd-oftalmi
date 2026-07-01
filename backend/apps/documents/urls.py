from django.urls import path

from .views import DocumentDetailView, DocumentListView


app_name = "documents"

urlpatterns = [
    path("", DocumentListView.as_view(), name="index"),
    path("<int:pk>/", DocumentDetailView.as_view(), name="detail"),
]
