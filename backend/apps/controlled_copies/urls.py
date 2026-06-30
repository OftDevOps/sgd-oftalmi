from django.urls import path

from .views import ControlledCopyIndexView


app_name = "controlled_copies"

urlpatterns = [
    path("", ControlledCopyIndexView.as_view(), name="index"),
]
