from django.urls import path

from .views import OrganizationalUnitDetailView, OrganizationalUnitListView


app_name = "organizational_units"

urlpatterns = [
    path("", OrganizationalUnitListView.as_view(), name="index"),
    path("<int:pk>/", OrganizationalUnitDetailView.as_view(), name="detail"),
]
