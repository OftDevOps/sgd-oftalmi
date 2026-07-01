from django.urls import path

from .views import (
    DocumentRequestCreateView,
    DocumentRequestDetailView,
    DocumentRequestListView,
)


app_name = "document_requests"

urlpatterns = [
    path("", DocumentRequestListView.as_view(), name="index"),
    path("new/", DocumentRequestCreateView.as_view(), name="create"),
    path("<int:pk>/", DocumentRequestDetailView.as_view(), name="detail"),
]
