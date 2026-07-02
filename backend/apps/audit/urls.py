from django.urls import path

from .views import AuditEventDetailView, AuditEventListView


app_name = "audit"

urlpatterns = [
    path("", AuditEventListView.as_view(), name="index"),
    path("<int:pk>/", AuditEventDetailView.as_view(), name="detail"),
]
