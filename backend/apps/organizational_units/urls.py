from django.urls import path

from .views import OrganizationalUnitIndexView


app_name = "organizational_units"

urlpatterns = [
    path("", OrganizationalUnitIndexView.as_view(), name="index"),
]
