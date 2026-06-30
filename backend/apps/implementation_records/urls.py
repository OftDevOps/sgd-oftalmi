from django.urls import path

from .views import ImplementationRecordIndexView


app_name = "implementation_records"

urlpatterns = [
    path("", ImplementationRecordIndexView.as_view(), name="index"),
]
