from django.urls import path

from .views import AuditIndexView


app_name = "audit"

urlpatterns = [
    path("", AuditIndexView.as_view(), name="index"),
]
